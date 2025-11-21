from sqlmodel import Session, select
from src.models.companies import Companies
from src.schemas.company import UpdateCompany

def get_company_by_id(session: Session, id: int) -> Companies | None:
    return session.exec(select(Companies).where(Companies.company_id == id)).first()

def get_all_companies(session: Session): 
    return session.exec(select(Companies).where(Companies.company_type == "supplier")).all()

def update_company(session: Session, company_id: int, update_data: UpdateCompany) -> Companies | None:
    company = get_company_by_id(session, company_id)
    
    if not company:
        return None
    
    # Update only the fields that are provided
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(company, key, value)
    
    session.add(company)
    session.commit()
    session.refresh(company)
    
    return company