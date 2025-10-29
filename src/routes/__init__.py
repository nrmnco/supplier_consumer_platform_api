from src.routes.authentication import router as auth_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(auth_router)