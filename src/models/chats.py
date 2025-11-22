from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Chats(SQLModel, table=True):
    __tablename__ = "chats"

    chat_id: int | None = Field(primary_key=True, default=None)
    linking_id: int = Field(foreign_key="linkings.linking_id", nullable=False)
    order_id: int | None = Field(foreign_key="orders.order_id", default=None, nullable=True)

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    order: "Orders" = Relationship(back_populates="chats")
    linking: "Linkings" = Relationship(back_populates="chats")

    messages: list["Messages"] = Relationship(back_populates="chat")