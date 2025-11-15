from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.user import get_user_by_email
from src.cruds.company import get_company_by_id
from src.cruds.products import create_product, get_all_products, delete_product, update_product
from src.schemas.products import ProductSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def all_products(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    products = get_all_products(session)
    return {"products": products}

@router.post("/")
async def add_product(data: ProductSchema, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    company = get_company_by_id(session, user.company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    if user.role not in ("owner", "manager") and company.type != "supplier":
        raise HTTPException(status_code=403, detail="Insufficient permissions to create product")
    
    product = create_product(session, data, company.company_id)

    return {"message": "Product created successfully", "product": product}
    
@router.delete("/{product_id}")
async def delete_product(product_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    company = get_company_by_id(session, user.company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    if user.role not in ("owner", "manager") and company.type != "supplier":
        raise HTTPException(status_code=403, detail="Insufficient permissions to create product")

    delete_product(session, product_id)

    return {"message": f"Product with id {product_id} deleted successfully"}

@router.put("/{product_id}")
async def update_product(product_id: int, data: ProductSchema, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    company = get_company_by_id(session, user.company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    if user.role not in ("owner", "manager") and company.type != "supplier":
        raise HTTPException(status_code=403, detail="Insufficient permissions to create product")
    

    product = update_product(session, product_id, data)

    return {"message": "Product updated successfully", "product": product}
