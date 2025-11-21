from pydantic import BaseModel
from src.models.companies import CompanyStatus


class UpdateCompany(BaseModel):
    name: str | None = None
    description: str | None = None
    logo_url: str | None = None
    location: str | None = None
    status: CompanyStatus | None = None
