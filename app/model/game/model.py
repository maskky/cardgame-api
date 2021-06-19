import random
import os

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import List

from ..custom_schema import PydanticObjectId
from app.util.config import TOTAL_CARD
from app.util.error import ErrorHandler

class Board(BaseModel):
  value: Optional[int]
  flipped: bool

  @root_validator()
  def set_name(cls, values: Dict[str, Any]):
    if not values.get("flipped"):
      values.pop("value")

    return values

class Game(BaseModel):
  username: str
  board: list
  movement: int
  cleared: bool
  card_lefts: int

  @classmethod
  def new_game(cls, username):
    values = [i for i in range(TOTAL_CARD // 2)]
    values.extend(values)
    random.shuffle(values)

    board = []
    for value in values:
      card = {}
      card["value"] = value
      card["flipped"] = False
      board.append(card)

    game = Game(
      username = username,
      board = board,
      movement = 0,
      cleared = False,
      card_lefts = TOTAL_CARD)

    return game

  @classmethod
  def flip_card(cls, game, card):
    previous = game.get("previous_flip")
    board = game["board"]
    game["movement"] += 1

    if previous is None:
      if board[card]["flipped"]:
        raise ErrorHandler(name = "ALREADY_FLIPPED")
      board[card]["flipped"] = True
      game["previous_flip"] = card
    else:
      game.pop("previous_flip")

      if card == previous: raise ErrorHandler(name = "DUPLICATED_FLIP")
      if board[previous]["flipped"] and board[card]["flipped"]: raise ErrorHandler(name = "ALREADY_FLIPPED")
      
      if board[previous]["value"] == board[card]["value"]:
        board[previous]["flipped"] = board[card]["flipped"] = True
        game["card_lefts"] -= 2

      else:
        board[previous]["flipped"] = board[card]["flipped"] = False

      if game["card_lefts"] <= 0:
        game["cleared"] = True

    return game

  @classmethod
  def show_compared_card(cls, game, card, previous):
    board = game["board"]

    if previous is None:
      board[card]["flipped"] = True
    else:
      board[previous]["flipped"] = board[card]["flipped"] = True

    return game

class GameInResponse(BaseModel):
  username: str
  movement: int
  cleared: bool
  user_best: int = None
  global_best: int = None
  board: List[Board]