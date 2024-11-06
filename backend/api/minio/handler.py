import os
import uuid
from io import BytesIO
from typing import Any

import fastapi
from fastapi import APIRouter, UploadFile, File, Depends
from starlette import status
from starlette.requests import Request
from minio import Minio
from starlette.responses import StreamingResponse, Response

from api.minio.schemas import GetFile, FilesSchema
from common.response.response_chema import ResponseModel, response_base
from common.response.response_code import CustomResponseCode

router = APIRouter()


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.get(
    "/file",
    summary="get file",
    description="return link to file",
    # responses={
    #     status.HTTP_200_OK: {
    #         "model": ResponseModel, # custom pydantic model for 200 response
    #         "description": "Ok Response",
    #     },
    # },
)
async def hello_world(
    request: Request,
    file: GetFile = Depends(),
) -> Response:
    minio_client = Minio(
        'minio:9000',
        access_key='9BiPgbQ1nlaYPRLwCwBk',
        secret_key='J5ECRM34lASo7ztaEwfwkilqG8oZkMeUuuT8VLRw',
        secure=False
    )

    # response = minio_client.get_object('images', file.file)
    # return StreamingResponse(BytesIO(response.read()))

    try:
        response = minio_client.get_object('images', file.file)
        return StreamingResponse(BytesIO(response.read()))
    except Exception as e:
        return StreamingResponse(status_code=404, content="")
        # return await response_base.fail(res=CustomResponseCode.HTTP_404)


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
    request: Request,
) -> Response:
    minio_client = Minio(
        'minio:9000',
        access_key='9BiPgbQ1nlaYPRLwCwBk',
        secret_key='J5ECRM34lASo7ztaEwfwkilqG8oZkMeUuuT8VLRw',
        secure=False
    )

    files = []

    buckets = minio_client.list_buckets()
    for bucket in buckets:
        # print(bucket.name, bucket.creation_date)
        # List objects information.
        objects = minio_client.list_objects(bucket.name)
        for obj in objects:
            print(obj.object_name)
            files.append(f"{bucket}/{obj.object_name}")

    files_schema = FilesSchema()
    files_schema.urls = files

    return await response_base.success(
        # data={"files": files_schema}
        data=files_schema
        # data={"files": "one"}
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
async def file(file: UploadFile = File(...)) -> ResponseModel:
    minio_client = Minio(
        'minio:9000',
        access_key='9BiPgbQ1nlaYPRLwCwBk',
        secret_key='J5ECRM34lASo7ztaEwfwkilqG8oZkMeUuuT8VLRw',
        secure=False
    )

    if not allowed_file(file.filename):
        raise response_base.fail(
            status_code=400,
            detail="Invalid file extension. Allowed extensions are txt, pdf, png, jpg, jpeg, gif."
        )

    file_size = os.fstat(file.file.fileno()).st_size
    extension = file.filename.rsplit('.', 1)[1].lower()
    uuid_filename = str(uuid.uuid4())
    file_name = f"{uuid_filename}.{extension}"
    # ret = minio_client.put_object('images', file.filename, file.file, file_size, content_type='image/jpeg')
    ret = minio_client.put_object('images', file_name, file.file, file_size, content_type='image/jpeg')

    return await response_base.success(
        data={
            'status' : 'success',
            'data': {
                'file': f'http://127.0.0.1:9000/{ret.bucket_name}/{ret.object_name}'
            }
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

    # if not allowed_file(file.filename):
    #     raise response_base.fail(
    #         status_code=400,
    #         detail="Invalid file extension. Allowed extensions are txt, pdf, png, jpg, jpeg, gif."
    #     )

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
