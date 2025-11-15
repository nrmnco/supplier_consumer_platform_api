from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token

router = APIRouter(prefix="/linkings", tags=["linkgings"])

@router.post("/")
async def add_linking(company_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    pass

