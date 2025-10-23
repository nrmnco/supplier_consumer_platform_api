from sqlmodel import SQLModel
from src.models.users import UserRole, Locale
from src.models.companies import CompanyType

class CompanySchema(SQLModel):
    name: str
    description: str | None = None
    logo_url: str | None = None
    location: str
    company_type: CompanyType

class UserSchema(SQLModel):
    first_name: str
    last_name: str
    phone_number: str

    email: str
    password: str
    role: UserRole
    locale: Locale

class UserCompanySchema(SQLModel):
    company: CompanySchema
    user: UserSchema

class UserLoginSchema(SQLModel):
    email: str
    password: str