import csv
import json
from datetime import datetime
from io import StringIO
from typing import Generic, Literal, Optional, TypeVar

from dateutil.parser import isoparse
from dateutil.tz import tzlocal
from dateutil.utils import default_tzinfo
from pydantic import create_model
from pydantic.generics import GenericModel
from pydantic.schema import schema

T = TypeVar("T")

class Error(GenericModel, Generic[T]):
    data  : Literal[None] = None
    error : T

    class Config:
        extra = "allow"

class OK(GenericModel, Generic[T]):
    data  : Optional[T]
    error : Literal[None] = None

    class Config:
        extra = "allow"

class IsoDatetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, datetime):
            if v.tzinfo is None:
                return default_tzinfo(v, tzlocal())

            return v
        else:
            return isoparse(v).astimezone()


def unfold_all(defs, schema):
    if isinstance(schema, dict):
        while "$ref" in schema:
            ref  = schema.pop("$ref")
            refn = ref[14:]

            schema.update(defs[refn])
        else:
            for sub in schema.values():
                unfold_all(defs, sub)
    elif isinstance(schema, list):
        for sub in schema:
            unfold_all(defs, sub)
    else:
        return


class GenericMeta(type):
    def __getitem__(self, t):
        m = create_model("V", v=(t, ...))
        s = schema([m])

        V = s["definitions"].pop("V")

        v = V["properties"]["v"]
        unfold_all(s["definitions"], v)

        if "title" in v:
            del v["title"]

        return type(self.__name__, (self,), {
            "__generic_model__"  : m,
            "__generic_schema__" : v,
        })


class CommaSeparated(Generic[T], metaclass=GenericMeta):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            **cls.__generic_schema__,
            title = "Comma Separated Values"
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, list):
            pass
        elif isinstance(v, str):
            r = csv.reader(StringIO(v))
            # only read the first line
            v = next(r)
        else:
            raise ValueError("list or comma seperated string expected")

        return cls.__generic_model__(v=v).v

class JsonStr(Generic[T], metaclass=GenericMeta):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            **cls.__generic_schema__,
            title = "JSON String"
        )

    @classmethod
    def validate(cls, v):
        try:
            obj = json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("invalid json string")

        # only use the validating effect, not the return value
        cls.__generic_model__(v=obj)

        return v
