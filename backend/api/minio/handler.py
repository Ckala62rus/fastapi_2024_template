import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)
from starlette import status
from starlette.requests import Request
from minio import (
    Minio,
    S3Error
)
from starlette.responses import Response

from api.minio.schemas import (
    GetFile,
    FilesSchema,
    Bucket
)
from api.minio.service import MinioService
from common.response.response_chema import (
    ResponseModel,
    response_base
)
from common.response.response_code import CustomResponseCode

router = APIRouter()


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.get(
    "/file",
    summary="get file",
    description="return link to file",
)
async def file(
    file: GetFile = Depends(),
) -> Response:

    minio_service = MinioService()
    try:
        return await minio_service.get_file_url(file.bucket, file.file)
    except S3Error as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data={
                "image": file.file,
                "message": e.message,
                "code": e.code
            }
        )


@router.get(
    "/files",
    summary="get files",
    description="get files from bucket",
    responses={
        status.HTTP_200_OK: {
            "model": FilesSchema, # custom pydantic model for 200 response
            "description": "Ok Response",
        },
    },
)
async def files(
    bucket: Bucket = Depends()
) -> Response:
    try:
        minio_service = MinioService()
        files = await minio_service.get_files_from_bucket(bucket.bucket)
        files_schema = FilesSchema().urls = files
    except Exception as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data={
                "message": e.detail,
            }
        )

    return await response_base.success(
        data=files_schema
    )


@router.post(
    "/file",
    summary="upload file",
    description="upload file",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel, # custom pydantic model for 200 response
            "description": "Ok Response",
        },
    },
)
async def file(
    nested_path: str = None,
    file: UploadFile = File(...),
    bucket: Bucket = Depends()
) -> ResponseModel:
    if not allowed_file(file.filename):
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data={
                "message": "Invalid file extension. Allowed extensions are txt, pdf, png, jpg, jpeg, gif."
            }
        )

    minio_service = MinioService()
    try:
        response_file = await minio_service.save_file(bucket.bucket, file, nested_path)
        return await response_base.success(
            data={
                'status': 'success',
                'data': {
                    'file': f'http://127.0.0.1:9000/{response_file.bucket_name}/{response_file.object_name}'
                }
            }
        )
    except S3Error as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data={
                "image": file.file,
                "message": e.message,
                "code": e.code
            }
        )


@router.post(
    "/videos",
    summary="upload video file",
    description="upload video file and return link on it",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel, # custom pydantic model for 200 response
            "description": "Ok Response",
        },
    },
)
async def video_file_upload(video: UploadFile = File(...)) -> ResponseModel:
    minio_client = Minio(
        'minio:9000',
        access_key='9BiPgbQ1nlaYPRLwCwBk',
        secret_key='J5ECRM34lASo7ztaEwfwkilqG8oZkMeUuuT8VLRw',
        secure=False
    )

    file_size = os.fstat(video.file.fileno()).st_size
    extension = video.filename.rsplit('.', 1)[1].lower()
    uuid_filename = str(uuid.uuid4())
    file_name = f"{uuid_filename}.{extension}"
    ret = minio_client.put_object('video', file_name, video.file, file_size, content_type='video/mp4')

    return await response_base.success(
        data={
            'status' : 'success',
            'data': {
                'file': f'http://127.0.0.1:9000/{ret.bucket_name}/{ret.object_name}'
            }
        }
    )
