from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId

class PydanticObjectId(BsonObjectId):

  @classmethod
  def __get_validators__(cls):
    yield cls.validate

  @classmethod
  def validate(cls, v):
    if not isinstance(v, BsonObjectId):
      raise TypeError('ObjectId required')
    return str(v)

  @classmethod
  def __modify_schema__(cls, field_schema):
    field_schema.update(type='string')

class User(BaseModel):
  username: str
  password: str
  create_at: Optional[datetime] = None
  update_at: Optional[datetime] = None

class UserInResponse(BaseModel):
  id: PydanticObjectId = Field(..., alias='_id')
  username: str
  create_at: datetime
  update_at: datetime
  