from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

ERROR = {
  "ALREADY_FLIPPED": {
    "status": 400,
    "message": "This card already flipped."
  },
  "DUPLICATED_FLIP": {
    "status": 400,
    "message": "Duplicate previous flip."
  },
  "GAME_ENDED": {
    "status": 400,
    "message": "This game was ended."
  },
  "INVALID_TOKEN": {
    "status": 401,
    "message": "Invalid access token."
  },
  "BAD_CREDENTIAL": {
    "status": 401,
    "message": "Incorrect username or password."
  },
  "GAME_NOT_FOUND": {
    "status": 404,
    "message": "You need to new game before play."
  },
  "DUPLICATED": {
    "status": 409,
    "message": "Duplicate username."
  }
}

class ErrorHandler(Exception):
  def __init__(self, name: str):
    self.name = name

    if (ERROR.get(name) is not None):
      self.status = ERROR[name]["status"]
      self.message = ERROR[name]["message"]
    else:
      self.status = 500
      self.message = "Internal server error."

@app.exception_handler(ErrorHandler)
async def send_error_response(request: Request, exc: ErrorHandler):
  return JSONResponse(
    status_code = exc.status,
    content = { "code": exc.status, "status": exc.name, "message": exc.message },
  )