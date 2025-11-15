from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/products")
async def all_products(company_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    pass
