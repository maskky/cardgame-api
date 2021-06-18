from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

ERROR = {
  "INVALID_TOKEN": {
    "STATUS": 401,
    "MESSAGE": "Invalid access token."
  },
  "BAD_CREDENTIAL": {
    "STATUS": 401,
    "MESSAGE": "Incorrect username or password."
  },
  "NOT_FOUND": {
    "STATUS": 404,
    "MESSAGE": "User not found."
  },
  "DUPLICATED": {
    "STATUS": 409,
    "MESSAGE": "Duplicate username."
  }
}

class ErrorHandler(Exception):
  def __init__(self, name: str):
    self.name = name

    if (ERROR.get(name) is not None):
      self.status = ERROR[name]["STATUS"]
      self.message = ERROR[name]["MESSAGE"]
    else:
      self.status = 500
      self.message = "Internal server error."

@app.exception_handler(ErrorHandler)
async def send_error_response(request: Request, exc: ErrorHandler):
  return JSONResponse(
    status_code = exc.status,
    content = { "code": exc.status, "status": exc.name, "message": exc.message },
  )