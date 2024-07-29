from typing import Annotated

from fastapi import Depends
from pymongo import MongoClient

from common.log import log
from core.config import settings


async def mongo_db() -> MongoClient:
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]
    try:
        yield db
    except Exception as e:
        log.error(e)
    finally:
        client.close()

MongoDB = Annotated[MongoClient, Depends(mongo_db)]
