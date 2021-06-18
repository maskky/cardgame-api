from motor.motor_asyncio import AsyncIOMotorClient
from .db import db

async def connect_to_mongo():
  db.client = AsyncIOMotorClient(str("mongodb://localhost:27017"))
  print("Connected to database.")

async def close_mongo_connection():
  db.client.close()
  print("Disconnected from database.")