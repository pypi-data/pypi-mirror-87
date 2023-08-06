import datetime
from functools import wraps

from sqlalchemy import MetaData
from sqlalchemy.orm.session import sessionmaker

Datetime = datetime.datetime


class _Empty: ...


def operation(func):
    @wraps(func)
    def wrapper(instance: MetaData, op, session=None):
        instance.ensure_table_exists(op)

        commit = session is None
        session: Session = session or sessionmaker(bind=instance.bind)()
        ret = func(instance, op, session)
        if commit:
            session.commit()
        if ret == _Empty:
            return None
        return ret or instance

    return wrapper
