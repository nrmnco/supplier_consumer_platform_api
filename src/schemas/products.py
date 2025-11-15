from enum import Enum
from sqlmodel import SQLModel



class ProductSchema(SQLModel):
    name: str
    description: str
    picture_url: list[str]
    
    stock_quantity: int
    retail_price: int
    threshold: int
    bulk_price: int
    minimum_order: int
    unit: str
