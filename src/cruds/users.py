from sqlmodel import Session, select
from src.models.users import Users
from src.database import get_session

def get_users(session: Session):
    users = session.exec(select(Users)).all()
    return users

def create_user(session: Session, user_data: dict):
    new_user = Users(**user_data)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user