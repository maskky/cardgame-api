from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..custom_schema import PydanticObjectId

class User(BaseModel):
  username: str
  password: str
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

class UserInRequest(BaseModel):
  username: str
  password: str

class UserInResponse(BaseModel):
  id: PydanticObjectId = Field(..., alias = "_id")
  username: str
  created_at: datetime
  updated_at: datetime
  