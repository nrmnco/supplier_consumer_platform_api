from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from src.core.database import get_session
from src.core.security import check_access_token
from src.schemas.order import OrderCreate, OrderStatusUpdate
from src.models.orders import OrderStatus
from src.cruds.order import (
    create_order,
    get_orders_for_company
)
from src.cruds.user import get_user_by_email
from src.cruds.company import get_company_by_id
from src.cruds.linkings import check_if_linked, get_linking

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/")
def create_new_order(order_data: OrderCreate, supplier_company_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])

    company = get_company_by_id(session, user.company_id)

    if company.company_type == "supplier":
        raise HTTPException(status_code=403, detail="Supplier can not order")
    
    if not check_if_linked(session, user.user_id, supplier_company_id):
        raise HTTPException(status_code=403, detail="Companies are not linked")
    
    linking = get_linking(session, user.company_id, supplier_company_id)
    
    try:
        order = create_order(order_data, linking.linking_id, user.user_id, session)
        return {"order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_all_orders(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])

    return get_orders_for_company(user.company_id, session)


# @router.get("/{order_id}", response_model=OrderRead)
# def get_order(order_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
#     user = get_user_by_email(session, user['sub'])
    
#     order = get_order_by_id(order_id, session)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order


# @router.patch("/{order_id}/status", response_model=OrderRead)
# def change_order_status(
#     order_id: int,
#     update_data: OrderStatusUpdate,
#     user: str = Depends(check_access_token),
#     session: Session = Depends(get_session)
# ):
#     user = get_user_by_email(session, user['sub'])

#     company = get_company_by_id(session, user.company_id)

#     if company.company_type == "supplier":
#         raise HTTPException(status_code=403, detail="Supplier can not order")
    

#     if update_data.status not in OrderStatus.__members__:
#         raise HTTPException(status_code=400, detail="Invalid status")

#     try:
#         order = update_order_status(
#             order_id,
#             OrderStatus(update_data.status),
#             session
#         )
#         return order
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))