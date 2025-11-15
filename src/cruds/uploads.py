from sqlmodel import Session, select
from src.models.companies import Companies


def store_company_url(session: Session, company_id: int, file_url: str):
    stmt = select(Companies).where(Companies.company_id == company_id)
    company = session.exec(stmt).one_or_none()

    if not company:
        raise ValueError("Company not found")

    company.logo_url = file_url
    session.add(company)
    session.commit()
    session.refresh(company)

    return company