from contextlib import asynccontextmanager

from fastapi import FastAPI

__all__ = ['register_app']

from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from core.path_conf import STATIC_DIR

from middleware.access_middleware import AccessMiddleware

from utils.serializer import MsgSpecJSONResponse
from api.router import router as main_router


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    Жизненный цикл FastApi. Сдесь можно закрывать соединения с БД, Redis

    :return:
    """
    print("Run app")

    yield

    print("Stop app")
    #await redis_client.close()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init, # todo почитать в документации
    )

    register_static_file(app)
    register_middleware(app)

    return app


def register_static_file(app: FastAPI):
    """
    nginx

    :param app:
    :return:
    """
    if settings.STATIC_FILES:
        import os

        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app: FastAPI):
    # Access log handler
    if settings.MIDDLEWARE_ACCESS:
        app.add_middleware(AccessMiddleware)

    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
