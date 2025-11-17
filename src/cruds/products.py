from sqlmodel import Session, select
from src.models.products import Products
from src.schemas.products import ProductSchema

def get_all_products(session: Session, company_id: int) -> list[Products]:
    products = session.exec(select(Products).where((Products.is_available == True) & (Products.company_id == company_id))).all()
    return products

def get_product_by_id(session: Session, product_id: int) -> list[Products]:
    product = session.get(Products, product_id)
    return product

def create_product(session: Session, data: ProductSchema, company_id: int) -> Products:
    product_data = data

    # Create product instance
    company = Products(**product_data.model_dump(), company_id=company_id)
    session.add(company)
    session.flush()

    session.commit()
    session.refresh(company)

    return company

def delete_product(session: Session, product_id: int) -> None:
    product = session.get(Products, product_id)

    if product:
        product.is_available = False
        session.commit()

def update_product(session: Session, product_id: int, data: ProductSchema) -> Products:
    product = session.get(Products, product_id)

    if not product:
        raise ValueError("Product not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)

    return product
