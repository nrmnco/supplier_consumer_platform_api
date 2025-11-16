import boto3
from uuid import uuid4

from src.core.config import settings



class S3Service:

    def __init__(self):
        self.bucket_name = settings.S3_BUCKET_NAME

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            )
        
    def create_post_url(self, ext: str = "jpg"):
        
        key = f"uploads/{uuid4()}.{ext}"

        url = self.s3.generate_presigned_post(
            Bucket=self.bucket_name,
            Key=key,
            Conditions=[],
            ExpiresIn=120
        )

        finalurl = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

        return url, finalurl
    
    def delete_file_by_url(self, url: str):
        try:
            url_splitted = url.split("/")
            key = url_splitted[-2] + "/" + url_splitted[-1]

            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True
        except Exception as e:
            print("Error deleting S3 object:", e)
            return False

s3_service = S3Service()