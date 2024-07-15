from fastapi import APIRouter

from core.config import settings
from .example.router import route as example_router
from .user.router import route as user_router


router = APIRouter(prefix=settings.API_V1_STR)

router.include_router(example_router)
router.include_router(user_router)
