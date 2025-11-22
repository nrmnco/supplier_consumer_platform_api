from sqlmodel import Session, select
from datetime import datetime

from src.models.chats import Chats
from src.models.messages import Messages, MessageType
from src.models.linkings import Linkings
from src.models.orders import Orders
from src.models.users import Users, UserRole


def get_or_create_chat_for_linking(session: Session, linking_id: int) -> Chats:
    chat = session.exec(
        select(Chats).where(Chats.linking_id == linking_id, Chats.order_id.is_(None))
    ).first()
    
    if not chat:
        chat = Chats(
            linking_id=linking_id,
            order_id=None
        )
        session.add(chat)
        session.commit()
        session.refresh(chat)
    
    return chat


def get_chat_for_order(session: Session, order_id: int) -> Chats | None:
    """Get the chat for a specific order"""
    chat = session.exec(
        select(Chats).where(Chats.order_id == order_id)
    ).first()
    return chat


def create_message(
    session: Session,
    chat_id: int,
    sender_id: int,
    body: str,
    message_type: MessageType = MessageType.text
) -> Messages:
    message = Messages(
        chat_id=chat_id,
        sender_id=sender_id,
        type=message_type,
        body=body
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_messages_for_chat(session: Session, chat_id: int, limit: int = 100, offset: int = 0):
    statement = (
        select(Messages)
        .where(Messages.chat_id == chat_id)
        .order_by(Messages.sent_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return session.exec(statement).all()


def check_user_can_chat(session: Session, user_id: int, linking_id: int) -> bool:
    linking = session.get(Linkings, linking_id)
    if not linking:
        return False

    if linking.status != "accepted":
        return False
    
    if linking.requested_by_user_id == user_id:
        return True
    
    if linking.assigned_salesman_user_id == user_id:
        return True
    
    return False


def check_user_can_access_order_chat(session: Session, user_id: int, order_id: int) -> bool:
    """Check if user can access order chat"""
    order = session.get(Orders, order_id)
    if not order:
        return False
    
    linking = session.get(Linkings, order.linking_id)
    if not linking:
        return False
    
    user = session.get(Users, user_id)
    if not user:
        return False
    
    # Consumer who created the order
    if order.consumer_staff_id == user_id:
        return True
    
    # Assigned salesman
    if linking.assigned_salesman_user_id == user_id:
        return True
    
    # Managers and owners from supplier company
    if user.role in [UserRole.manager, UserRole.owner]:
        if user.company_id == linking.supplier_company_id:
            return True
    
    return False


def create_system_message(
    session: Session,
    order_id: int,
    user_id: int,
    message_type: MessageType,
    body_data: dict
) -> Messages | None:
    """Create a system message for an order chat"""
    import json
    
    # Get the chat for this order
    chat = get_chat_for_order(session, order_id)
    if not chat:
        # If chat doesn't exist (shouldn't happen for orders), try to create/get it
        # But get_chat_for_order doesn't create. 
        # We assume chat exists because it's created with order.
        return None
        
    message = Messages(
        chat_id=chat.chat_id,
        sender_id=user_id,
        type=message_type,
        body=json.dumps(body_data)
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message
