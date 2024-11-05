from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/minio', tags=["Minio"])

route.include_router(router)
