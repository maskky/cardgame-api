from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

def response_model(model: BaseModel) -> JSONResponse:
  return JSONResponse(content = jsonable_encoder(model, by_alias=True))