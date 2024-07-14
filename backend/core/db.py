from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings

async_engine = create_async_engine(
    # postgresql+asyncpg проверить
    url=settings.SQLALCHEMY_DATABASE_URL,
    # url="postgresql+psycopg://pguser:000000@localhost:5432/mydb",
    echo=True,
    # pool_size=5,
    # max_overflow=10
)

SessionLocal = async_sessionmaker(async_engine)
Engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
