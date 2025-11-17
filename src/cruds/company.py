from sqlmodel import Session, select
from src.models.companies import Companies

def get_company_by_id(session: Session, id: int) -> Companies | None:
    return session.exec(select(Companies).where(Companies.company_id == id)).first()

def get_all_companies(session: Session): 
    return session.exec(select(Companies).where(Companies.company_type == "supplier")).all()