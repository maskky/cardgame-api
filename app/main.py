from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .util.error import ErrorHandler, send_error_response
from .api.index import router as api_router
from .adapter.mongo.connection import connect_to_mongo, close_mongo_connection

app = FastAPI(title = "CardGame API")

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
app.add_exception_handler(ErrorHandler, send_error_response)
app.include_router(api_router, prefix = "/api/v1")
