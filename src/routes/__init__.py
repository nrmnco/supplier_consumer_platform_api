from src.routes.authentication import router as auth_router
from src.routes.uploads import router as uploads_router
from src.routes.user import router as user_router
from src.routes.city import router as city_router
from src.routes.company import router as company_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(auth_router)
router.include_router(uploads_router)
router.include_router(user_router)
router.include_router(city_router)
router.include_router(company_router)
