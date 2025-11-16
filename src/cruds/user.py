from sqlmodel import Session, select
from src.core.security import hash_password
from src.models.users import Users, UserStatus
from src.schemas.authentication import UserSchema
from src.schemas.update_user import UpdateUserSchema

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

def update_user(session: Session, updated_user: UpdateUserSchema, user_id: int) -> Users:
    user = session.get(Users, user_id)
    password = updated_user.hashed_password
    updated_user.hashed_password = hash_password(password)

    for key, value in updated_user.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user