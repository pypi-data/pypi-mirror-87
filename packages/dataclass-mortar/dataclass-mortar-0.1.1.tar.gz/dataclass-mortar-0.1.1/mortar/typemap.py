from typing import Type, Union, Text, List, get_args, get_origin, Any
from sqlalchemy.sql.sqltypes import NullType, DateTime, Float, JSON, Integer, String
from .util import Datetime
from dataclasses import dataclass, is_dataclass, fields, Field, field
from sqlalchemy.types import TypeEngine

alchamey_type = {
    Text: String,
    List: String,
    Datetime: DateTime,
    float: Float,
    int: Integer,
    dict: JSON
}


def python_to_alechamy(a_type):
    generic_type = get_origin(a_type)
    if generic_type:
        if generic_type in (dict, list):
            return JSON
        template = list(get_args(a_type))
        if generic_type == Union:
            try:
                template.remove(type(None))
            except ValueError:
                ...  # no worries if it isn't in there.
            if len(template) == 1:
                return python_to_alechamy(template[0])
        else:
            a_type = generic_type
    try:
        if issubclass(a_type, TypeEngine) or is_dataclass(a_type):
            return a_type
    except TypeError:
        ...

    return alchamey_type.get(a_type, String)