from pydantic import BaseModel
from typing import List, Optional
from src.models.messages import MessageType

class MessageResponse(BaseModel):
    message_id: int
    sender_id: int
    body: str
    type: MessageType
    sent_at: str

class ChatHistoryResponse(BaseModel):
    chat_id: int
    linking_id: Optional[int] = None
    order_id: Optional[int] = None
    messages: List[MessageResponse]
    limit: int
    offset: int
