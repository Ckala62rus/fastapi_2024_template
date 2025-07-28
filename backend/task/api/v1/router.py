from fastapi import APIRouter

from task.api.v1.handler import router as router_handler

route = APIRouter(prefix='/task', tags=["⚡ Tasks"])

route.include_router(router_handler)
