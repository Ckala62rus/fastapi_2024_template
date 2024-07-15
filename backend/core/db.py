import sys
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from common.log import log
from core.config import settings

Base = declarative_base()

def create_engine_and_session(url: str | URL):
    try:
        # Core database
        engine = create_async_engine(url, echo=True, future=True, pool_pre_ping=True)
        # log.success('success connect to database')
    except Exception as e:
        log.error('❌ Error to connect database {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session

async_engine, async_db_session = create_engine_and_session(settings.SQLALCHEMY_DATABASE_URL)

async def get_db() -> AsyncSession:
    """session generator"""
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()

# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]
