from sqlmodel import SQLModel
from typing import List, Optional
from datetime import datetime


class OrderProductCreate(SQLModel):
    # identify product by name (no client-supplied DB ids)
    product_name: str
    quantity: int


class OrderCreate(SQLModel):
    supplier_company_id: int
    products: List[OrderProductCreate]


class OrderStatusUpdate(SQLModel):
    status: str


class OrderReadProduct(SQLModel):
    product_id: int
    product_name: str
    quantity: int
    price: int


class OrderRead(SQLModel):
    order_id: int
    status: str
    total_price: int
    products: List[OrderReadProduct]
    created_at: datetime
    updated_at: datetime


class OrderListRead(SQLModel):
    orders: List[OrderRead]