from motor.motor_asyncio import AsyncIOMotorClient

from .db import db
from app.util.config import MONGODB_URL

async def connect_to_mongo():
  db.client = AsyncIOMotorClient(MONGODB_URL)
  print("Connected to database.")

async def close_mongo_connection():
  db.client.close()
  print("Disconnected from database.")