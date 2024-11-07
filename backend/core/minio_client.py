from minio import Minio
from minio.error import S3Error

from common.log import log
from core.config import settings


def minio_client() -> Minio:
    """
    Minio client
    :return: Minio
    """
    client = Minio(
        settings.MINIO_HOST,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.SECURE
    )

    try:
        return client
    except S3Error as e:
        log.error(e)
