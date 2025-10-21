from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class CompanyStatus(str, Enum):
    active = "active"
    suspended = "suspended"

class CompanyType(str, Enum):
    supplier = "supplier"
    consumer = "consumer"

class Companies(SQLModel, table=True):
    __tablename__ = "companies"

    company_id: int | None = Field(primary_key=True, default=None)

    status: CompanyStatus = Field(default=CompanyStatus.active, nullable=False)

    name: str = Field(nullable=False)
    description: str | None = Field(default=None, nullable=True)
    logo_url: str | None = Field(default=None, nullable=True)
    location: str = Field(nullable=False)
    company_type: CompanyType = Field(nullable=False)

    users: list["Users"] = Relationship(back_populates="company")
    products: list["Prodcuts"] = Relationship(back_populates="company")
    
    linked_as_consumer: list["Linkings"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.consumer_company_id]"})
    linked_as_supplier: list["Linkings"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.supplier_company_id]"})

    