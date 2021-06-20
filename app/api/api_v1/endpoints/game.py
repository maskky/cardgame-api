import os

from fastapi import APIRouter, Depends, Header, Path
from starlette.status import HTTP_200_OK

from app.adapter.mongo.db import AsyncIOMotorClient, get_database
from app.model.game.model import GameInResponse, Game
from app.model.game.function import create_or_update_game, get_current_game, update_game
from app.model.token.function import decode_access_token
from app.model.score.function import create_or_update_best_score, get_user_best_score, get_global_best_score
from app.api.api_v1.response import response_model, response_success
from app.util.config import TOTAL_CARD
from app.util.error import ErrorHandler

router = APIRouter()

@router.get("/new_game", response_model = GameInResponse, tags = ["Game"], status_code = HTTP_200_OK)
async def new_game(authorization: str = Header(None), db: AsyncIOMotorClient = Depends(get_database)):
  decoded_token = await decode_access_token(authorization)
  game = await create_or_update_game(db, decoded_token.username)

  user_best_score = await get_user_best_score(db, decoded_token.username)
  global_best_score = await get_global_best_score(db)

  game["user_best"] = user_best_score
  game["global_best"] = global_best_score
  
  return response_model(GameInResponse.parse_obj(game))

@router.get("/continue", response_model = GameInResponse, tags = ["Game"], status_code = HTTP_200_OK)
async def continue_game(authorization: str = Header(None), db: AsyncIOMotorClient = Depends(get_database)):
  decoded_token = await decode_access_token(authorization)
  game = await get_current_game(db, decoded_token.username)
  
  if game is None:
    raise ErrorHandler(name = 'GAME_NOT_FOUND')

  user_best_score = await get_user_best_score(db, decoded_token.username)
  global_best_score = await get_global_best_score(db)

  game["user_best"] = user_best_score
  game["global_best"] = global_best_score

  return response_model(GameInResponse.parse_obj(game))


@router.get("/flip_card/{card_id}", response_model = GameInResponse, tags = ["Game"], status_code = HTTP_200_OK)
async def flip_card(authorization: str = Header(None), card_id: int = Path(..., ge = 0, lt = TOTAL_CARD), db: AsyncIOMotorClient = Depends(get_database)):
  decoded_token = await decode_access_token(authorization)
  found_game = await get_current_game(db, decoded_token.username)
  
  if found_game is None or found_game["cleared"]:
    raise ErrorHandler(name = 'GAME_NOT_FOUND')
  
  previous_flip = found_game.get("previous_flip")

  game = Game.flip_card(found_game, int(card_id))
  if game["cleared"]:
    await create_or_update_best_score(db, decoded_token.username, game["movement"])
  
  await update_game(db, found_game["_id"], game)

  game = Game.show_compared_card(found_game, int(card_id), previous_flip)

  user_best_score = await get_user_best_score(db, decoded_token.username)
  global_best_score = await get_global_best_score(db)

  game["user_best"] = user_best_score
  game["global_best"] = global_best_score

  return response_model(GameInResponse.parse_obj(game))