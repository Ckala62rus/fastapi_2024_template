from fastapi import APIRouter

from core.config import settings
from .example.router import route as example_router


router = APIRouter(prefix=settings.API_V1_STR)

router.include_router(example_router)
