from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.core.database import get_session
from src.cruds.authentication import create_company_with_owner, authenticate_user
from src.schemas.authentication import UserCompanySchema, UserLoginSchema
from src.core.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
async def register_company_with_owner(data: UserCompanySchema, session: Session = Depends(get_session)):
    try:
        owner_user = create_company_with_owner(session, data)
        return {"message": "Company and owner user created successfully", "owner_user_id": owner_user.user_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=dict)
async def login_user(data: UserLoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(session, data.email, data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    token = create_access_token(data={"sub": user.email})
    
    return {"access_token": token, "token_type": "bearer"}
