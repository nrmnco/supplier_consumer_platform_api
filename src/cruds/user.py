from sqlmodel import Session, select
from src.models.users import Users

def get_user_by_email(session: Session, email: str) -> Users | None:
    return session.exec(select(Users).where(Users.email == email)).first()

def get_user_by_id(session: Session, user_id: str) -> Users | None:
    return session.exec(select(Users).where(Users.user_id == user_id)).first()

def get_user_by_phone(session: Session, phone_number: str):
    return session.exec(select(Users).where(Users.phone_number == phone_number)).first()

def get_all_users(session: Session, company_id: int):
    return session.exec(select(Users).where(Users.company_id == company_id)).all()
