from sqlmodel import Session, select
from datetime import datetime

from src.models.chats import Chats
from src.models.messages import Messages, MessageType
from src.models.linkings import Linkings


def get_or_create_chat_for_linking(session: Session, linking_id: int) -> Chats:
    chat = session.exec(
        select(Chats).where(Chats.linking_id == linking_id)
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

