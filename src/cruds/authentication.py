from sqlmodel import Session
from src.models.users import Users
from src.models.companies import Companies
from src.schemas.authentication import UserCompanySchema
from src.core.security import hash_password, verify_password
from src.cruds.user import get_user_by_email

def create_company_with_owner(session: Session, data: UserCompanySchema) -> Users:
    company_data = data.company
    owner_data = data.user

    # Create company instance
    company = Companies(**company_data.model_dump())
    session.add(company)
    session.flush()

    # Create owner user instance linked to the company
    owner_user = Users(company_id=company.company_id, 
                       **owner_data.model_dump(exclude={'password'}),
                       hashed_password=hash_password(owner_data.password))
    session.add(owner_user)
    session.commit()
    session.refresh(owner_user)

    return owner_user


def authenticate_user(session: Session, email: str, password: str) -> Users | None:
    user = get_user_by_email(session, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


