from fastapi import APIRouter, Depends, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.adapter.mongo.db import AsyncIOMotorClient, get_database
from app.model.user.function import create_user, get_user_by_username, check_duplicate_username
from app.model.token.function import create_access_token, decode_access_token
from app.model.user.model import UserInRequest, UserInResponse
from app.model.token.model import Token
from app.util.index import hash_password, verify_password
from app.api.api_v1.response import response_model
from app.util.error import ErrorHandler

router = APIRouter()

@router.post("/register", response_model = UserInResponse, tags = ["User"], status_code = HTTP_201_CREATED)
async def register(user: UserInRequest, db: AsyncIOMotorClient = Depends(get_database)):
  if await check_duplicate_username(db, user.username):
    raise ErrorHandler(name = "DUPLICATED")

  user.password = hash_password(user.password)
  created_user = await create_user(db, user.username, user.password)

  return response_model(UserInResponse.parse_obj(created_user))

@router.post("/login", response_model = Token, tags = ["User"], status_code = HTTP_200_OK)
async def login(user: UserInRequest, db: AsyncIOMotorClient = Depends(get_database)):
  found_user = await get_user_by_username(db, user.username)

  if not found_user:
    raise ErrorHandler(name = "BAD_CREDENTIAL")

  if not verify_password(user.password, found_user["password"]):
    raise ErrorHandler(name = "BAD_CREDENTIAL")
  
  access_token = create_access_token(data = { "sub": user.username })

  return response_model(Token.parse_obj(access_token))

@router.get("/me", response_model = UserInResponse, tags = ["User"], status_code = HTTP_200_OK)
async def get_current_user(authorization: str = Header(None), db: AsyncIOMotorClient = Depends(get_database)):
  decoded_token = await decode_access_token(authorization)
  found_user = await get_user_by_username(db, decoded_token.username)

  return response_model(UserInResponse.parse_obj(found_user))