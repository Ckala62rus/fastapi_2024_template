from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/user', tags=["User"])

route.include_router(router)
