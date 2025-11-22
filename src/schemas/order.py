from sqlmodel import SQLModel
from typing import List
from datetime import datetime

class OrderProductCreate(SQLModel):
    product_id: int
    quantity: int


class OrderCreate(SQLModel):
    products: List[OrderProductCreate]


class OrderStatusUpdate(SQLModel):
    status: str


class OrderReadProduct(SQLModel):
    product_id: int
    quantity: int
    price: int


class OrderRead(SQLModel):
    order_id: int
    linking_id: int
    consumer_staff_id: int
    total_price: int
    status: str
    created_at: str
    updated_at: str

