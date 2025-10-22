from sqlmodel import SQLModel, Field, Relationship  
from enum import Enum
from datetime import datetime

class LinkingStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    unlinked = "unlinked"

class Linkings(SQLModel, table=True):
    __tablename__ = "linkings"

    linking_id: int | None = Field(primary_key=True, default=None)
    consumer_company_id: int = Field(foreign_key="companies.company_id", nullable=False)
    supplier_company_id: int = Field(foreign_key="companies.company_id", nullable=False)

    requested_by_user_id: int = Field(foreign_key="users.user_id", nullable=False)
    responded_by_user_id: int | None = Field(foreign_key="users.user_id", default=None, nullable=True)
    assigned_salesman_user_id: int | None = Field(foreign_key="users.user_id", default=None, nullable=True)
    
    status: LinkingStatus = Field(default=LinkingStatus.pending, nullable=False)
    message: str | None = Field(default=None, nullable=True)

    created_at: str = Field(default=datetime.now(), nullable=False)
    updated_at: str = Field(default=datetime.now(), nullable=False)

    consumer_company: "Companies" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.consumer_company_id]"})
    supplier_company: "Companies" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.supplier_company_id]"})

    requested_by_user: "Users" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.requested_by_user_id]"})
    responded_by_user: "Users" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.responded_by_user_id]"})
    assigned_salesman_user: "Users" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Linkings.assigned_salesman_user_id]"})

    orders: list["Orders"] = Relationship(back_populates="linking")

    chats: list["Chats"] = Relationship(back_populates="linking")
