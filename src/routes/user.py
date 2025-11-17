from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import check_access_token
from src.cruds.user import delete_user, get_user_by_email, get_user_by_id, get_user_by_phone, get_all_users, create_user, update_user
from src.models.users import UserRole
from src.schemas.authentication import UserSchema
from src.schemas.update_user import UpdateUserSchema


router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
async def read_current_user(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    email = user.get("sub")

    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/get-user")
async def read_all_users(user_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    user = get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/")
async def all_users(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    email = user.get("sub")
    
    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role not in (UserRole.owner, UserRole.manager):
        raise HTTPException(status_code=403, detail="Insufficient permissions to view all users")
    
    users = get_all_users(session, user.company_id)
    
    return {"users": users}



@router.post("/")
async def add_user(new_user: UserSchema, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    email = user.get("sub")
    
    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == UserRole.staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions to add new users")
    
    if user.role == UserRole.manager and new_user.role != UserRole.staff:
        raise HTTPException(status_code=403, detail="Managers can only add staff users")
    
    if new_user.role == UserRole.owner:
        raise HTTPException(status_code=403, detail="Cannot create another owner user")
    
    if get_user_by_email(session, new_user.email):
        raise HTTPException(status_code=400, detail="A user with this email already exists")
    
    if get_user_by_phone(session, new_user.phone_number):
        raise HTTPException(status_code=400, detail="A user with this phone number already exists")

    new_user1 = create_user(session, new_user, user.company_id)

    return {"users": new_user1}

@router.delete("/{user_id}")
async def remove_user(user_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    email = user.get("sub")
    
    requesting_user = get_user_by_email(session, email)

    if not requesting_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if requesting_user.role == UserRole.staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions to delete users")
    
    user_to_delete = get_user_by_id(session, user_id)

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User to delete not found")

    if requesting_user.role == UserRole.manager and user_to_delete.role != UserRole.staff:
            raise HTTPException(status_code=403, detail="Managers can only delete staff users")
    
    if requesting_user.user_id == user_id:
        raise HTTPException(status_code=400, detail="Users cannot delete themselves")
    
    success = delete_user(session, user_to_delete)
    if not success:
        raise HTTPException(status_code=404, detail="User to delete not found")
    
    return {"message": "User deleted successfully"}

@router.put("/{user_id}")
async def put_user(updated_user: UpdateUserSchema, user_id: int, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    email = user.get("sub")

    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if get_user_by_email(session, updated_user.email)and user.email != updated_user.email:
        raise HTTPException(status_code=409, detail="This email already exists")
    
    if get_user_by_phone(session, updated_user.phone_number) and user.phone_number != updated_user.phone_number:
        raise HTTPException(status_code=409, detail="This phone already exists")
    
    if user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Can not update another user's profile")
    
    result_user = update_user(session, updated_user, user_id)     

    return {"user": result_user}
    
