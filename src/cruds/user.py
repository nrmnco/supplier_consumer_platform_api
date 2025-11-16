from sqlmodel import Session, select
from src.core.security import hash_password
from src.models.users import Users, UserStatus
from src.schemas.authentication import UserSchema

def get_user_by_email(session: Session, email: str) -> Users | None:
    return session.exec(select(Users).where(Users.email == email)).first()

def get_user_by_id(session: Session, user_id: str) -> Users | None:
    return session.exec(select(Users).where(Users.user_id == user_id)).first()

def get_user_by_phone(session: Session, phone_number: str):
    return session.exec(select(Users).where(Users.phone_number == phone_number)).first()

def get_all_users(session: Session, company_id: int):
    return session.exec(select(Users).where(Users.company_id == company_id)).all()

def create_user(session: Session, user: UserSchema, company_id: int) -> Users:
    user = Users(company_id=company_id, 
                       **user.model_dump(exclude={'password'}),
                       hashed_password=hash_password(user.password))
    session.add(user)
    session.flush()

    session.commit()
    session.refresh(user)

    return user

def delete_user(session: Session, user: Users) -> bool:
    if user:
        user.status = UserStatus.suspended
        session.commit()
        return True
    return False
