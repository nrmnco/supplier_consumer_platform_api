import jwt
from datetime import datetime, timedelta
from typing import Optional

from src.core.config import settings

def create_token(data: dict, expires_delta: Optional[timedelta] = None, refresh: Optional[bool] = False) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    if refresh:
        to_encode.update({"type": "refresh"})
    else:
        to_encode.update({"type": "access"})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str, refresh: Optional[bool] = False) -> dict:
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = decoded_jwt.get("sub")
        if email is None:
            raise ValueError("Invalid token: missing subject")
        if refresh and decoded_jwt.get("type") != "refresh":
            raise ValueError("Invalid token: not a refresh token")
        if not refresh and decoded_jwt.get("type") != "access":
            raise ValueError("Invalid token: not an access token")

        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
