import datetime
import inspect
import logging
from dataclasses import dataclass, is_dataclass, fields, Field, field
from functools import wraps, partial
from itertools import chain
from typing import Type, Union, Text, List, get_args, get_origin, Any

from sqlalchemy import Column, MetaData, Table, String, create_engine, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, Session, relationship, ColumnProperty, mapper
from sqlalchemy.orm.base import manager_of_class
from sqlalchemy.sql.sqltypes import NullType, DateTime, Float, JSON, Integer
from sqlalchemy.sql.type_api import TypeEngine

from .proxy import CallbackProxy
from .typemap import python_to_alechamy
from .util import operation
logger = logging.getLogger("mortar")

Datetime = datetime.datetime

class mortar(MetaData):
    tables_checked = []

    def __call__(self, item, *a, **kwargs):
        try:
            return item.__table__
        except:
            return self.defer_to_session(item)

    def engine(self, engine_or_string, **kw):
        if isinstance(engine_or_string, str):
            engine_or_string = create_engine(engine_or_string, **kw)
        self.bind = engine_or_string
        return self

    def ensure_table_exists(self, op):
        if not is_dataclass(op):
            return None
        tbl = op.__table__
        if tbl.name in self.tables_checked:
            return True
        if self.bind.has_table(tbl.name):
            self.tables_checked.append(tbl.name)
            return True
        else:
            self.create_all(tables=[tbl], checkfirst=False)
            self.tables_checked.append(tbl.name)
            return True

    @operation
    def save(self, instance, session=None):
        try:
            session.add_all([instance])
        except BaseException as ex:
            v = metadata.query(type(instance)).get(instance.course_id)
            print(v)
            raise
        return instance

    @operation
    def truncate(self, instance, session=None):
        session.execute(instance.__table__.delete())

    def __getattr__(self, item):
        if item in Session.__dict__:
            return self.defer_to_session(item)

    def defer_to_session(self, item):
        @operation
        def runner(s, o, ses):
            return getattr(ses, item)(o)

        return partial(runner, self)


metadata: Union[mortar, Session] = mortar()


def persist(cls=None, /, *, table=None, database=None) -> Union[Type]:
    closure_table = table

    def wrapper(cls):
        table = closure_table or Table(cls.__name__, database or metadata)
        return _process_class(cls, table)

    if cls is None:
        # parameters sent return the wrapper to decorate
        return wrapper

    # called with nothing as @persist we'll do everthing, return a processed class
    return wrapper(cls)


class _Empty: ...


class Getter(hybrid_property):
    _mortar_prop = True
    accepts_scalar_loader = False
    collection = None
    column_data = None
    supports_population = False

    @property
    def impl(self):
        return self

    def get(self, state, dict_, passive=None):
        return self.fget(state.object)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.fget(instance)

    def __init__(self, descriptor):
        super().__init__(descriptor)
        self.key = descriptor.__name__


class presitable_property(hybrid_property):
    _mortar_prop = True
    column_data = None


Base = declarative_base()


def persist_property(prp_or_column) -> Union[property, Any]:
    prp = None
    clm = None
    if isinstance(prp_or_column, Column):
        clm = prp_or_column
    else:
        prp = prp_or_column

    def wrapper(prp):
        p = Getter(prp)
        p._mortar_prop = True
        p.column_data = clm
        return p

    if prp is None:
        return wrapper

    return wrapper(prp)


def persisted_properties(datacls):
    for k, v in inspect.getmembers(datacls, lambda a: hasattr(a, "_mortar_prop")):
        # Everythiing is set up to use fields from dataclasses so sending a field here makes seense
        f = field()
        f.name = k
        f.type = Text
        f.metadata = {"_mortar_prop": True}
        if v.column_data is not None:
            f.metadata["mortar"] = {"column": v.column_data}

        # setattr(datacls, k, QueryableAttribute(datacls, k, v))
        yield f


def _before_insert(mapper, connection, target):
    target.__dict__["item_id"] = CallbackProxy(lambda: type(target).item_id.fget(target))


def _process_class(datacls, table: Table):
    if not is_dataclass(datacls):
        logging.getLogger("damp").warning(
            f"{datacls} wrapped with persist but is not a data class, making it a data class first"
        )
        datacls = dataclass(datacls)
    props = {}
    manual_register = []
    insert_listener = event.listen(datacls, 'before_insert', _before_insert)

    @event.listens_for(datacls, 'load')
    def enable_persist(target, context):
        target.__dict__["item_id"] = CallbackProxy(lambda: type(target).item_id.fget(target))

    for dt_field in chain(fields(datacls), persisted_properties(datacls)):
        field_type = python_to_alechamy(dt_field.type)
        if is_dataclass(field_type):
            keys = []
            for k in field_type.__table__.primary_key.columns:
                fkc = Column(dt_field.name + "_" + k.key, k.type, ForeignKey(k))
                keys.append(fkc)
                table.append_column(fkc)
            props[dt_field.name] = relationship(field_type, foreign_keys=keys)
        else:
            meta = mortar_meta(dt_field)
            column_def = column_factory(meta, dt_field, field_type)
            table.append_column(column_def)
            if meta.get("_mortar_prop"):
                manual_register.append(column_def.name)
                props = {column_def.name: ColumnProperty(column_def, _instrument=False)}
    datacls.save = lambda s, **kw: table.metadata.save(s, **kw)
    datacls.truncate = classmethod(table.metadata.truncate)
    if len(table.primary_key) == 0:
        pk = table.columns.get(f"item_id", Column('auto_id', String))
        pk.instrument = False
        pk.primary_key = True
        table.append_constraint(pk)
    datacls.__table__ = table
    datacls.__mapper__ = mapper(datacls, table, properties=props)
    manager = manager_of_class(datacls)

    for k in manual_register:
        manager.instrument_attribute(k, getattr(datacls, k))
    return datacls


def mortar_meta(dt_field: Field):
    meta = dt_field.metadata.copy()
    mort_meta = {}
    col_def = None
    if isinstance(meta, Column):
        col_def = meta
    else:
        mort_meta = meta.pop("mortar", mort_meta)
        for k in meta:
            if k[:7] == "_mortar":
                mort_meta[k] = meta[k]
    if col_def is not None:
        mort_meta["column"] = col_def
    return mort_meta


def column_factory(meta: dict, dt_field, field_type=None):
    column = meta.get("column", Column(dt_field.name))
    if not isinstance(column, Column):
        return column
    if column.name is None:
        column.name = dt_field.name
    if type(column.type) is NullType:
        logger.debug((dt_field.name, dt_field.type))
        column.type = field_type or python_to_alechamy(dt_field.type)
    try:
        return column.copy()
    except:
        return column
