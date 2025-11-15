from sqlmodel import Session, select
from src.models.products import Products
from src.schemas.products import ProductSchema

def get_all_products(session: Session) -> list[Products]:
    products = session.exec(select(Products)).all()
    return products

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
        session.delete(product)
        session.commit()

