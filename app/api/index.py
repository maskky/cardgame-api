from fastapi import APIRouter

from .api_v1.endpoints.user import router as user_router
from .api_v1.endpoints.game import router as game_router

router = APIRouter()
router.include_router(user_router)
router.include_router(game_router)
