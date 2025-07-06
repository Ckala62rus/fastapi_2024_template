from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/user', tags=["👤 Authentication", "👥 Users"])

route.include_router(router)
