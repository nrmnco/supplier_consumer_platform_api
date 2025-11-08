from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.user import get_user_by_email, get_user_by_id


router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
async def read_current_user(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    email = user.get("sub")

    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/get-user")
async def read_all_users(user_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
