from app.adapter.mongo.db import AsyncIOMotorClient
from app.util.index import get_current_datetime
from app.util.error import ErrorHandler
from .model import Score

DATABASE = 'score'
COLLECTION = 'document'

async def create_or_update_best_score(conn: AsyncIOMotorClient, username: str, score: int):
  found_score = await conn[DATABASE][COLLECTION].find_one({ "username": username })
  new_score = Score(username = username, score = score).dict()

  if found_score is None:
    await conn[DATABASE][COLLECTION].insert_one(new_score)
  else:
    if score < found_score["score"]:
      await conn[DATABASE][COLLECTION].replace_one({ "_id": found_score["_id"] }, new_score)
  
  return new_score

async def get_user_best_score(conn: AsyncIOMotorClient, username: str):
  found_score = await conn[DATABASE][COLLECTION].find_one({ "username": username })

  if found_score is None:
    score = None
  else:
    score = found_score["score"]

  return score

async def get_global_best_score(conn: AsyncIOMotorClient):
  found_score = conn[DATABASE][COLLECTION].find({}).sort("score")
  found_score = await found_score.to_list(length = 1)
  
  if len(found_score):
    best_score = found_score[0]["score"]
  else:
    best_score = None

  return best_score