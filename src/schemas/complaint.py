from pydantic import BaseModel
from src.models.complaints import ComplaintStatus


class CreateComplaint(BaseModel):
    description: str


class UpdateComplaintStatus(BaseModel):
    notes: str | None = None


class ResolveComplaint(BaseModel):
    resolution_notes: str
    cancel_order: bool = False  # If True, manager can cancel/reject the order
