import os
import uuid
from io import BytesIO

from fastapi import (
    UploadFile,
    HTTPException
)
from minio.error import S3Error
from minio.helpers import ObjectWriteResult
from starlette.responses import StreamingResponse

from common.log import log
from core.minio_client import minio_client

ALLOWED_EXTENSIONS_IMAGES = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file_images(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGES

class MinioService:
    def __init__(self):
        self.minio_client = minio_client()

    async def get_file_url(
        self,
        bucket_name: str,
        file_name: str
    ) -> StreamingResponse | S3Error:
        response = None
        try:
            response = minio_client().get_object(bucket_name, file_name)
            return StreamingResponse(BytesIO(response.read()))
        except S3Error as e:
            log.error(e.code)
            raise e
        finally:
            if response:
                response.close()
                response.release_conn()

    async def save_file(self, bucket_name: str, file: UploadFile)-> ObjectWriteResult:
        file_size = os.fstat(file.file.fileno()).st_size
        extension = file.filename.rsplit('.', 1)[1].lower()
        uuid_filename = str(uuid.uuid4())
        file_name = f"{uuid_filename}.{extension}"

        return minio_client().put_object(
            bucket_name,
            file_name,
            file.file,
            file_size,
            content_type='image/jpeg'
        )

    async def get_files_from_bucket(self, bucket_name: str) -> list:
        try:
            files = []
            objects = minio_client().list_objects(bucket_name, recursive=True)
            for obj in objects:
                files.append(f"{bucket_name}/{obj.object_name}")
            return files
        except S3Error as e:
            log.error(e)
            if 'code: NoSuchBucket' in str(e):
                raise HTTPException(status_code=404, detail=f"Bucket {bucket_name} not found")

    async def object_exist(file_path: str, bucket_name: str) -> bool:
        try:
            minio_client().stat_object(bucket_name, file_path)
            return True
        except Exception as error:
            if 'code: NoSuchKey' in str(error):
                return False
            else:
                raise error

    async def backet_create_if_not_exist(self, bucket_name: str) -> None:
        # Make the bucket if it doesn't exist.
        exist = minio_client().bucket_exists(bucket_name)
        if not exist:
            minio_client().make_bucket(bucket_name)
