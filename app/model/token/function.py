import os

from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException

from app.model.token.model import TokenData
from app.util.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from app.util.error import ErrorHandler

ALGORITHM = "HS256"
TOKEN_TYPE = "Bearer"
TOKEN_TYPE_INDEX = 0
TOKEN_INDEX = 1

def create_access_token(data: dict):
  expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes = 15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
  
  return { "access_token": encoded_jwt, "token_type": TOKEN_TYPE }

async def decode_access_token(authorization: str):
  try:
    token_type = authorization.split()[TOKEN_TYPE_INDEX]
    token = authorization.split()[TOKEN_INDEX]

    if token_type != TOKEN_TYPE:
      raise ErrorHandler(name = "INVALID_TOKEN")

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")

    if username is None:
      raise ErrorHandler(name = "INVALID_TOKEN")

    return TokenData(username = username)
  except:
    raise ErrorHandler(name = "INVALID_TOKEN")