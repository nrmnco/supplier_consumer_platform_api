from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.core.database import get_session
from src.cruds.city import get_all_cities
from src.core.security import check_access_token


router = APIRouter(prefix="/cities", tags=["Cities"])

@router.get("/get-all-cities")
async def get_cities(user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    cities = get_all_cities(session)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    
    return cities

