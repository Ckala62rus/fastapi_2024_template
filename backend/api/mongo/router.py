from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/mongo', tags=["🍃 MongoDB"])

route.include_router(router)
