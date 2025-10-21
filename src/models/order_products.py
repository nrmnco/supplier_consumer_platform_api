from sqlmodel import SQLModel, Field, Relationship

class OrderProducts(SQLModel, table=True):
    __tablename__ = "order_products"

    order_id: int = Field(foreign_key="orders.order_id", primary_key=True, nullable=False)
    product_id: int = Field(foreign_key="products.proudct_id", primary_key=True, nullable=False)

    product_quantity: int = Field(nullable=False)
    product_price: int = Field(nullable=False)

    order: "Orders" = Relationship(back_populates="order_products")
    product: "Products" = Relationship(back_populates="order_products")