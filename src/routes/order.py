from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from src.core.database import get_session
from src.core.security import check_access_token
from src.schemas.order import OrderCreate, OrderStatusUpdate, OrderRead
from src.models.orders import OrderStatus
from src.models.linkings import Linkings
from src.cruds.order import (
    create_order,
    get_orders_for_company,
    get_order_by_id,
    update_order_status,
    get_ordered_products_for_company,
    get_products_for_order,
    get_orders_by_linking_id
)
from src.cruds.user import get_user_by_email
from src.cruds.company import get_company_by_id
from src.cruds.linkings import check_if_linked, get_linking

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/")
async def create_new_order(order_data: OrderCreate, supplier_company_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
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

    return get_ordered_products_for_company(user.company_id, session)


@router.get("/{order_id}")
def get_order(order_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])
    
    order = get_order_by_id(order_id, session)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get the linking associated with the order
    linking = session.get(Linkings, order.linking_id)
    if not linking:
        raise HTTPException(status_code=404, detail="Linking not found")
    
    # Check if user's company is either consumer or supplier in the linking
    if user.company_id != linking.consumer_company_id and user.company_id != linking.supplier_company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get products for this order
    products = get_products_for_order(order_id, session)
    
    # Return order with products
    return {
        "order_id": order.order_id,
        "linking_id": order.linking_id,
        "consumer_staff_id": order.consumer_staff_id,
        "total_price": order.total_price,
        "status": order.status,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "products": products
    }


@router.patch("/{order_id}/status")
async def change_order_status(
    order_id: int,
    status: str,
    user: str = Depends(check_access_token),
    session: Session = Depends(get_session)
):
    user = get_user_by_email(session, user['sub'])

    # Get the order
    order = get_order_by_id(order_id, session)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get the linking associated with the order
    linking = session.get(Linkings, order.linking_id)
    if not linking:
        raise HTTPException(status_code=404, detail="Linking not found")
    
    # Check if user is from supplier company that is in the linking from order
    if user.company_id != linking.supplier_company_id:
        raise HTTPException(status_code=403, detail="Only supplier company can change order status")

    if status not in OrderStatus.__members__:
        raise HTTPException(status_code=400, detail="Invalid status")

    try:
        order, message = update_order_status(
            order_id,
            OrderStatus(status),
            user.user_id,
            session
        )
        
        # Broadcast system message if created
        if message:
            from src.routes.chat import broadcast_order_message
            
            broadcast_data = {
                "type": "message",
                "message_id": message.message_id,
                "chat_id": message.chat_id,
                "sender_id": message.sender_id,
                "sender_name": f"{user.first_name} {user.last_name}",
                "body": message.body,
                "message_type": message.type,
                "sent_at": message.sent_at
            }
            await broadcast_order_message(order.order_id, broadcast_data)
            
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/linking/{linking_id}", response_model=List[OrderRead])
def get_orders_by_linking(linking_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_email(session, user['sub'])
    
    linking = session.get(Linkings, linking_id)
    if not linking:
        raise HTTPException(status_code=404, detail="Linking not found")
    
    if user.company_id != linking.consumer_company_id and user.company_id != linking.supplier_company_id:
        raise HTTPException(status_code=403, detail="Access denied")
        
    return get_orders_by_linking_id(linking_id, session)