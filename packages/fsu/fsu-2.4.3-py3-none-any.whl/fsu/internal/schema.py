from typing import List, Any, Optional, Union, Literal, Tuple, TypeVar

from pydantic import BaseModel, Field, PositiveInt
from fsu.internal.util import cap2snake

class ObjectName(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return cap2snake(v)


T = TypeVar("T")

Fields0 = List[str] # no recursive typedef support, FUCK PYTHON!
Fields1 = List[Union[str, Tuple[str, Fields0]]]
Fields2 = List[Union[str, Tuple[str, Fields1]]]
Fields3 = List[Union[str, Tuple[str, Fields2]]]
Fields4 = List[Union[str, Tuple[str, Fields3]]]
Path    = List[str]

ComparisonOperator = Literal["EQ", "LIKE", "STARTS_WITH", "IN", "GT", "GE", "LT", "LE"]
ComparisonExpr     = Tuple[ComparisonOperator, Path, Any]
LeafExpr           = Tuple[T, List[ComparisonExpr]]
LogicalExpr        = Union[
                         Tuple[Literal["AND"], List[Union[ComparisonExpr, LeafExpr[Literal["OR"]]]]],
                         Tuple[Literal["OR"],  List[Union[ComparisonExpr, LeafExpr[Literal["AND"]]]]],
                     ]
Filter             = Union[LogicalExpr, ComparisonExpr]

Ordering = Literal["ASC", "DESC"]
Order    = List[Tuple[Ordering, Path]]

Values = List[Tuple[str, Any]]

class ReadMany(BaseModel):
    object  : ObjectName
    fields_ : Fields4 = Field(..., alias="fields")
    filter  : Optional[Filter]
    order   : Optional[Order] = [("DESC", ["id"])]
    page    : Optional[PositiveInt] = 1    # type: ignore
    size    : Optional[PositiveInt] = 1000 # type: ignore

class ReadOne(BaseModel):
    object  : ObjectName
    fields_ : Fields4 = Field(..., alias="fields")

class CreateOne(BaseModel):
    object : ObjectName
    values : Values

class UpdateMany(BaseModel):
    object : ObjectName
    values : Values
    filter : Filter

class UpdateOne(BaseModel):
    object : ObjectName
    values : Values

class DeleteMany(BaseModel):
    object : ObjectName
    filter : Filter

class DeleteOne(BaseModel):
    object : ObjectName

class LoginIn(BaseModel):
    code : str

class LoginOut(BaseModel):
    access_token : str

class GetCurrentUserOut(BaseModel):
    id   : int
    name : str
