from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.company import get_company_by_id
from src.cruds.user import get_user_by_email
from src.cruds.linkings import create_linking
from src.schemas.linkings import LinkingSchema

router = APIRouter(prefix="/linkings", tags=["linkgings"])

@router.post("/")
async def add_linking(company_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    company = get_company_by_id(session, user.company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    if company.type != "consumer":
        raise HTTPException(status_code=403, detail="Insufficient permissions to send linking request")
    
    linking = create_linking(session, LinkingSchema(), consumer_company_id=company.company_id, requested_user_id=user.user_id, company_id=company_id)

    return {"message": "Linking request created successfully", "linking": linking}

