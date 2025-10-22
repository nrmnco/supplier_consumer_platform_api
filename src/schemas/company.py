from sqlmodel import SQLModel
from src.models.companies import CompanyType

class CompanyCreate(SQLModel):
    name: str
    description: str | None = None
    logo_url: str | None = None
    location: str
    company_type: CompanyType