from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/permission', tags=["🛡️ Permissions"])

route.include_router(router)
