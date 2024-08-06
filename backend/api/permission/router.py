from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/permissions', tags=["Permission"])

route.include_router(router)
