from io import BytesIO
from minio.error import S3Error
from starlette.responses import StreamingResponse

from common.log import log
from core.minio_client import minio_client


class MinioService:
    def __init__(self):
        self.minio_client = minio_client()

    async def get_file_url(
        self,
        bucket_name: str,
        file_name: str
    ) -> StreamingResponse | S3Error:
        try:
            response = minio_client().get_object(bucket_name, file_name)
            return StreamingResponse(BytesIO(response.read()))
        except S3Error as e:
            log.error(e.code)
            raise e
