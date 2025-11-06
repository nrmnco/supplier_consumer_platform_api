from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.jwt import decode_token

from pwdlib  import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

security = HTTPBearer()

def check_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    
    try:
        decoded_token = decode_token(token, refresh=False)
        return decoded_token
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def check_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    
    try:
        decoded_token = decode_token(token, refresh=True)
        return decoded_token
    
    except Exception as e:
        raise Exception(f"Refresh token is invalid: {str(e)}")

