from fastapi import FastAPI

__all__ = ['register_app']

from core.config import settings
from core.path_conf import STATIC_DIR
from utils.serializer import MsgSpecJSONResponse


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
        # lifespan=register_init, // todo почитать в документации
    )

    register_static_file(app)

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
    pass

