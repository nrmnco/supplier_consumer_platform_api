from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime

class UserStatus(str, Enum):
    active = "active"
    suspended = "suspended"

class UserRole(str, Enum):
    owner = "owner"
    manager = "manager"
    staff = "staff"

class Locale(str, Enum):
    ru = "ru"
    en = "en"
    kz = "kz"

class Users(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int | None = Field(primary_key=True, default=None)
    company_id: int = Field(foreign_key="companies.company_id", default=None)

    status: UserStatus = Field(default=UserStatus.active, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    phone_number: str = Field(nullable=False, index=True, unique=True)

    email: str = Field(nullable=False, index=True, unique=True)
    hashed_password: str = Field(nullable=False)
    role: UserRole = Field(nullable=False)

    created_at: str = Field(default=datetime.now() ,nullable=False)
    locale: Locale = Field(default=Locale.en, nullable=False)

    company: "Companies" = Relationship(back_populates="users")

    requested_linkings: list["Linkings"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.requested_by_user_id]"})
    responded_linkings: list["Linkings"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.responded_by_user_id]"})
    assigned_salesman_linkings: list["Linkings"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.assigned_salesman_user_id]"})

    orders: list["Orders"] = Relationship(back_populates="consumer_staff")