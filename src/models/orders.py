from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime

class OrderStatus(str, Enum):
    created = "created"
    processing = "processing"
    shipping = "shipping"
    completed = "completed"

class Orders(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: int | None = Field(primary_key=True, default=None)
    linking_id: int = Field(foreign_key="linkings.linking_id", nullable=False)
    consumer_staff_id: int = Field(foreign_key= "users.used_id", nullable=False)

    total_proce: int = Field(nullable=False)

    status: OrderStatus = Field(default=OrderStatus.created, nullable=False)

    created_at: str = Field(default=datetime.now(), nullable=False)
    updated_at: str = Field(default=datetime.now(), nullable=False)

    linking: "Linkings" = Relationship(back_populates="orders")
    consumer_staff: "Users" = Relationship(back_populates="orders")

    order_products: list["OrderProducts"] = Relationship(back_populates="order")