from typing import Annotated, Any
from bson import ObjectId
import datetime
from pydantic_core import core_schema
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue

from pydantic import BaseModel
from pydantic.v1.json import ENCODERS_BY_TYPE
ENCODERS_BY_TYPE[ObjectId]=str

class Item(BaseModel):
  msg: str


class ObjectIdPydanticAnnotation:
  @classmethod
  def validate_object_id(cls, v: Any, handler) -> ObjectId:
    if isinstance(v, ObjectId):
      return v

    s = handler(v)
    if ObjectId.is_valid(s):
      return ObjectId(s)
    else:
      raise ValueError("Invalid ObjectId")

  @classmethod
  def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
    assert source_type is ObjectId
    return core_schema.no_info_wrap_validator_function(cls.validate_object_id, core_schema.str_schema(), serialization=core_schema.to_string_ser_schema())

  @classmethod
  def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
    return handler(core_schema.str_schema())


class Notification(BaseModel):
  message: str
  is_read: bool = False,
  created: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


class User(BaseModel):
  id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias="_id")
  userId: str
  notifications: list[Notification] = []


