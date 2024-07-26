from fastapi import APIRouter

from .handler import router

route = APIRouter(prefix='/mongo', tags=["Mongo"])

route.include_router(router)
