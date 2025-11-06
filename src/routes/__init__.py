from src.routes.authentication import router as auth_router
from src.routes.uploads import router as uploads_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(auth_router)
router.include_router(uploads_router)
