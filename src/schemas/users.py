from sqlmodel import Field, SQLModel
from src.models.users import UserRole, Locale

class UserCreate(SQLModel):
    first_name: str = Field()
    last_name: str
    phone_number: str
    email: str
    password: str
    role: UserRole
    locale: Locale = Locale.en