from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.company import get_company_by_id, get_all_companies, update_company
from src.cruds.user import get_user_by_email
from src.schemas.company import UpdateCompany
from src.models.users import UserRole

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


@router.put("/{company_id}")
async def update_company_route(
    company_id: int,
    update_data: UpdateCompany,
    user: dict = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    """
    Update company information. Only the owner of the company can update it.
    """
    # Get the authenticated user
    user_obj = get_user_by_email(session, user['sub'])
    
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the company exists
    company = get_company_by_id(session, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify that the user belongs to this company
    if user_obj.company_id != company_id:
        raise HTTPException(
            status_code=403, 
            detail="You can only update your own company"
        )
    
    # Verify that the user is the owner
    if user_obj.role != UserRole.owner:
        raise HTTPException(
            status_code=403, 
            detail="Only the company owner can update company information"
        )
    
    # Update the company
    updated_company = update_company(session, company_id, update_data)
    
    if not updated_company:
        raise HTTPException(status_code=500, detail="Failed to update company")
    
    return {
        "message": "Company updated successfully",
        "company": updated_company
    }