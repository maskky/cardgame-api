from fastapi import APIRouter

from .user.index import router as user_router

router = APIRouter()
router.include_router(user_router)
