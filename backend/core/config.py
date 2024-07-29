from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

from core.path_conf import BasePath


class Settings(BaseSettings):
    """Global Settings"""

    model_config = SettingsConfigDict(
        env_file=f'{BasePath}/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Env Config
    ENVIRONMENT: Literal['dev', 'pro']

    # DateTime
    DATETIME_TIMEZONE: str = 'Europe/Moscow'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_ACCESS: bool = False

    # Env MySQL
    # MYSQL_HOST: str
    # MYSQL_PORT: int
    # MYSQL_USER: str
    # MYSQL_PASSWORD: str

    # POSTGRES
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'postgres'
    POSTGRES_PORT: str = '5432'
    POSTGRES_HOST: str = 'db_fastapi_2024'
    # POSTGRES_HOST_ALEMBIC: str = '127.0.0.1'
    SQLALCHEMY_DATABASE_URL: str = f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_DATABASE_URL_FOR_ALEMBIC: str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    # Env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # Redis
    REDIS_TIMEOUT: int = 5

    # FastAPI
    API_V1_STR: str = '/api/v1'
    TITLE: str = 'FastAPI'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'FastAPI Best Architecture'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'

    @model_validator(mode='before')
    @classmethod
    def validate_openapi_url(cls, values):
        if values['ENVIRONMENT'] == 'prod':
            values['OPENAPI_URL'] = None
        return values

    # Static Server
    STATIC_FILES: bool = False

    # Token
    TOKEN_ALGORITHM: str = 'HS256'  # алгоритм
    # TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # Единица измерения в секундах
    TOKEN_EXPIRE_SECONDS: int = 60 * 2  # Минута
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Время жизни рефреш токена в секундах
    TOKEN_REDIS_PREFIX: str = 'fba_token'
    TOKEN_REFRESH_REDIS_PREFIX: str = 'fba_refresh_token'
    TOKEN_EXCLUDE: list[str] = [  # JWT / RBAC 白名单
        f'{API_V1_STR}/auth/login',
    ]

    # JWT
    JWT_SECRET: str = 'veryVerySecretKey'
    JWT_ALGORITHM: str = 'HS256'
    TOKEN_TIME_EXPIRES: int = 60

    # Log
    LOG_STDOUT_FILENAME: str = 'fba_access.log'
    LOG_STDERR_FILENAME: str = 'fba_error.log'

    # Mongo
    MONGO_USER_API: str = "root"
    MONGO_PASSWORD_API: str = "M0ngo100500"
    MONGO_HOST_API: str = "mongo"
    MONGO_URI: str = f'mongodb://{MONGO_USER_API}:{MONGO_PASSWORD_API}@{MONGO_HOST_API}'
    MONGO_DB: str


# Декоратор lru_cache для хэширования конфига, что бы при следующих обращениях брался его кеш
@lru_cache
def get_settings() -> Settings:
    """
    Load settings from env
    :return:
    """
    return Settings()


# Создание экземпляра конфигурационного класса
settings = get_settings()
