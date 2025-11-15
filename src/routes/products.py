from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.user import get_user_by_email
from src.cruds.company import get_company_by_id
from src.cruds.products import create_product, get_all_products
from src.schemas.products import ProductSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/products")
async def all_products(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    products = get_all_products(session)
    return {"products": products}

@router.post("/products")
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
    
