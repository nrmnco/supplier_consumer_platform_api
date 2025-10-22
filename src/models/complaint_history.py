from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum

class ComplaintStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    escalated = "escalated"
    resolved = "resolved"
    closed = "closed"

class ComplaintHistory(SQLModel, table=True):
    __tablename__ = "complaint_history"

    history_id: int | None = Field(primary_key=True, default=None)
    complaint_id: int = Field(foreign_key="complaints.complaint_id", nullable=False)
    changed_by_user_id: int = Field(foreign_key="users.user_id", nullable=False)

    new_status: ComplaintStatus = Field(nullable=False)
    notes: str | None = Field(default=None, nullable=True)

    updated_at: str = Field(default=datetime.now(), nullable=False)

    complaint: "Complaints" = Relationship(back_populates="history")