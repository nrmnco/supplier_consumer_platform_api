from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.company import get_company_by_id, get_all_companies
from src.cruds.user import get_user_by_email

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("/get-company")
async def get_company(company_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    company = get_company_by_id(session, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company


@router.get("/")
async def get_companis(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])
    company = get_company_by_id(session, user.company_id)

    if company.company_type != "consumer":
        return HTTPException(status_code=403, detail="Not enough rights")
    
    companies = get_all_companies(session)

    return {"companies": companies}