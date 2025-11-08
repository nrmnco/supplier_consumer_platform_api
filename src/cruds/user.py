from sqlmodel import Session, select
from src.models.users import Users

def get_user_by_email(session: Session, email: str) -> Users | None:
    return session.exec(select(Users).where(Users.email == email)).first()

def get_user_by_id(session: Session, user_id: str) -> Users | None:
    return session.exec(select(Users).where(Users.user_id == user_id)).first()

