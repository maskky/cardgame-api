from app.adapter.mongo.db import AsyncIOMotorClient
from app.util.index import get_current_datetime
from app.util.error import ErrorHandler
from .model import Game

DATABASE = 'game'
COLLECTION = 'document'

async def create_or_update_game(conn: AsyncIOMotorClient, username: str):
  found_game = await conn[DATABASE][COLLECTION].find_one({ "username": username })
  new_game = Game.new_game(username).dict()

  if found_game is None:
    await conn[DATABASE][COLLECTION].insert_one(new_game)
  else:
    await conn[DATABASE][COLLECTION].replace_one({ "_id": found_game["_id"] }, new_game)
  
  return new_game

async def get_current_game(conn: AsyncIOMotorClient, username: str):
  found_game = await conn[DATABASE][COLLECTION].find_one({ "username": username })

  return found_game

async def update_game(conn: AsyncIOMotorClient, _id = str, game = Game):
  updated_game = await conn[DATABASE][COLLECTION].replace_one({ "_id": _id }, game)
  
  return updated_game
