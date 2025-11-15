from sqlmodel import SQLModel, Field, Relationship

class Products(SQLModel, table=True):
    __tablename__ = "products"

    product_id: int | None = Field(primary_key=True, default=None)
    company_id: int | None = Field(foreign_key="companies.company_id", default=None)

    name: str = Field(nullable=False)
    description: str | None = Field(default=None, nullable=True)
    picture_url: str | None = Field(default=None, nullable=True)
    stock_quantity: int = Field(nullable=False, default=0)
    
    retail_price: int = Field(nullable=False)
    threshold: int | None = Field(nullable=True, default=None)
    bulk_price: int | None = Field(nullable=True, default=None)

    minimum_order: int = Field(nullable=False, default=1)
    unit: str = Field(nullable=False)

    company: "Companies" = Relationship(back_populates="products")
    order_products: list["OrderProducts"] = Relationship(back_populates="product")