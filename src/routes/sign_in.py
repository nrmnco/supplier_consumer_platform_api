from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/sign-up", tags=["sign-up"])

@router.post("/")
async def sign_up():
    return {"message": "Sign-up endpoint"}

