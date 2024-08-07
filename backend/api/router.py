from fastapi import APIRouter

from core.config import settings
from .example.router import route as example_router
from .user.router import route as user_router
from task.api.v1.router import route as task_router
from .mongo.router import route as mongo_router
from .permission.router import route as permission_router

router = APIRouter(prefix=settings.API_V1_STR)

router.include_router(example_router)
router.include_router(user_router)
router.include_router(task_router)
router.include_router(mongo_router)
router.include_router(permission_router)
