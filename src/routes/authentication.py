from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.core.database import get_session
from src.cruds.authentication import create_company_with_owner, authenticate_user
from src.cruds.user import get_user_by_phone, get_user_by_email
from src.schemas.authentication import UserCompanySchema, UserLoginSchema
from src.core.jwt import create_token, decode_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
async def register_company_with_owner(data: UserCompanySchema, session: Session = Depends(get_session)):
    user = get_user_by_email(session, data.user.email)

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    
    user = get_user_by_phone(session, data.user.phone_number)

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this phone number already exists")

    try:
        user = create_company_with_owner(session, data)
        access_token = create_token(data={"sub": user.email})
        refresh_token = create_token(data={"sub": user.email}, expires_delta=timedelta(days=7), refresh=True)
        return {"company_id": user.company_id, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=dict)
async def login_user(data: UserLoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(session, data.email, data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    access_token = create_token(data={"sub": user.email})
    refresh_token = create_token(data={"sub": user.email}, expires_delta=timedelta(days=7), refresh=True)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=dict)
async def refresh_token(refresh_token: str, session: Session = Depends(get_session)):
    try:
        decoded = decode_token(refresh_token, refresh=True)
        email = decoded.get("sub")
        user = get_user_by_email(session, email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    access_token = create_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}