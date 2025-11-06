from fastapi import APIRouter, Depends

from src.services.s3_service import s3_service
from src.core.security import check_access_token

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.get("/upload-url")
async def get_upload_url(ext: str, user: str = Depends(check_access_token)):
    put_url, finalurl = s3_service.create_post_url(ext)
    return {"put_url": put_url, "finalurl": finalurl}

@router.post("/store-url")
async def store_file_url(file_url: str, user: str = Depends(check_access_token)):
    pass
    # return {"message": "File URL stored successfully", "file_url": file_url}