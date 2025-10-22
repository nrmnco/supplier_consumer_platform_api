from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime

class ComplaintStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    escalated = "escalated"
    resolved = "resolved"
    closed = "closed"

class Complaints(SQLModel, table=True):
    __tablename__ = "complaints"

    complaint_id: int | None = Field(primary_key=True, default=None)
    order_id: int = Field(foreign_key="orders.order_id", nullable=False)
    assigned_to_salesman_id: int = Field(foreign_key="users.user_id", nullable=False)
    escalated_to_manager_id: int | None = Field(foreign_key="users.user_id", default=None, nullable=True)
    escalated_to_owner_id: int | None = Field(foreign_key="users.user_id", default=None, nullable=True)

    status: ComplaintStatus = Field(default=ComplaintStatus.open, nullable=False)
    
    description: str = Field(nullable=False)
    resolution_notes: str | None = Field(default=None, nullable=True)

    created_at: str = Field(default=datetime.now(), nullable=False)
    updated_at: str = Field(default=datetime.now(), nullable=False)

    order: "Orders" = Relationship(back_populates="complaints")
    assigned_to_salesman: "Users" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Complaints.assigned_to_salesman_id]"})
    escalated_to_manager: "Users" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Complaints.escalated_to_manager_id]"})
    escalated_to_owner: "Users" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Complaints.escalated_to_owner_id]"})

    history: list["ComplaintHistory"] = Relationship(back_populates="complaint")