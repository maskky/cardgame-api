from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..custom_schema import PydanticObjectId

class Score(BaseModel):
  username: str
  score: int

class ScoreInResponse(BaseModel):
  id: PydanticObjectId = Field(..., alias='_id')
  username: str
  created_at: datetime
  updated_at: datetime
  