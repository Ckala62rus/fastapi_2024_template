from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/example', tags=["Example"])

route.include_router(router)
