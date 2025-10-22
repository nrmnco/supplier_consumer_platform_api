from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime

class MessageType(str, Enum):
    text = "text"
    audio = "audio"
    image = "image"
    file = "file"

class Messages(SQLModel, table=True):
    __tablename__ = "messages"
    
    message_id: int | None = Field(primary_key=True, default=None)
    chat_id: int = Field(foreign_key="chats.chat_id", nullable=False)
    sender_id: int = Field(foreign_key="users.user_id", nullable=False)

    type: MessageType = Field(default=MessageType.text, nullable=False)
    body: str = Field(nullable=False)
    sent_at: str = Field(default=datetime.now(), nullable=False)

    chat: "Chats" = Relationship(back_populates="messages")