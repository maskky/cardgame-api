from app.adapter.mongo.db import AsyncIOMotorClient
from app.util.index import get_current_datetime

DATABASE = "user"
COLLECTION = "document"

async def check_duplicate_username(conn: AsyncIOMotorClient, username: str):
  user = await conn[DATABASE][COLLECTION].find_one({
    "username": username
  })

  return False if user is None else True

async def create_user(conn: AsyncIOMotorClient, username: str, password: str):
  created_user = await conn[DATABASE][COLLECTION].insert_one({
    "username": username,
    "password": password,
    "created_at": get_current_datetime(),
    "updated_at": get_current_datetime()
  })

  user = await conn[DATABASE][COLLECTION].find_one({
    "_id": created_user.inserted_id
  })
  user.pop("password")

  return user

async def get_user_by_username(conn: AsyncIOMotorClient, username: str):
  user = await conn[DATABASE][COLLECTION].find_one({
    "username": username
  })

  return user
