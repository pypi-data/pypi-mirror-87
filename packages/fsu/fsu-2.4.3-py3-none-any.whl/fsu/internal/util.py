from typing import Literal
from datetime import datetime
import re

from dateutil.tz import tzlocal
from dateutil.utils import default_tzinfo
from sqlalchemy.types import Integer, String, Text, DateTime, Enum, JSON, Numeric
from pydantic import create_model, conint, constr, condecimal
from fsu.schema import IsoDatetime

_cap_words_re = re.compile(f"[A-Z]+[^A-Z]*")
def cap2snake(s):
    return "_".join((w.lower() for w in _cap_words_re.findall(s)))


def create_field_def(column_def):
    type_ = column_def.type

    if type(type_) == Integer:
        return conint(ge=-2**31, le=2**31 - 1)
    elif type(type_) == String:
        return constr(max_length=type_.length)
    elif type(type_) == Text:
        return str
    elif type(type_) == DateTime:
        return IsoDatetime
    elif type(type_) == Enum:
        return type_.enum_class
    elif type(type_) == JSON:
        return dict
    elif type(type_) == Numeric:
        return condecimal(max_digits=type_.precision, decimal_places=type_.scale)
    else:
        return None

SchemaMode = Literal["auto", "loose", "strict"]
def create_schema(table, mode : SchemaMode = "auto"):
    field_defs = {
        k : v
        for k, v in {
            str(x.name) : (
                create_field_def(x),
                ... if mode == "strict" else
                None if mode == "loose" else
                None if x.nullable or x.autoincrement == True else
                ...,
            )
            for x in table.c
        }.items()
        if v[0] is not None
    }

    return create_model(str(table.name), **field_defs) # type: ignore

def normalize_datetime(v):
    if any(isinstance(v, t) for t in [dict, list]):
        return deep_normalize_datetime(v)
    elif isinstance(v, datetime):
        return default_tzinfo(v, tzlocal())
    else:
        return v

def deep_normalize_datetime(d):
    if isinstance(d, dict):
        return {
            k : normalize_datetime(d[k])
            for k in d
        }
    elif isinstance(d, list):
        return [
            normalize_datetime(v)
            for v in d
        ]
