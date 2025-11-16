from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.core.database import get_session
from src.services.s3_service import s3_service
from src.core.security import check_access_token
from src.cruds.uploads import store_company_url

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.get("/upload-url")
async def get_upload_url(ext: str, user: str = Depends(check_access_token)):
    put_url, finalurl = s3_service.create_post_url(ext)
    return {"put_url": put_url, "finalurl": finalurl}

@router.post("/companies/{company_id}/photo")
async def store_company_photo(company_id: int, file_url: str, user: str = Depends(check_access_token), session: Session = Depends(get_session)):
    updated_company = store_company_url(session, company_id, file_url)
    return {"message": "Logo stored successfully", "company": updated_company}

@router.delete("/delete-file")
async def delete_file(file_url: str, user: str = Depends(check_access_token)):
    success = s3_service.delete_file_by_url(file_url)
    if success:
        return {"message": "File deleted successfully"}
    else:
        return {"message": "Failed to delete file"}
