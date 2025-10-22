from sqlmodel import Session
from src.models.companies import Companies
from src.schemas.company import CompanyCreate

def company_create(session: Session, company_data: CompanyCreate):
    new_company = Companies(**company_data.model_dump())
    session.add(new_company)
    session.commit()
    session.refresh(new_company)
    return new_company