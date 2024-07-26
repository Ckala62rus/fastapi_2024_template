from random import randint
import pymongo

from fastapi import (
    APIRouter,
    Depends
)

from api.mongo.schemas import (
    UpdateDateMongoDBSchema,
    MongoPaginateSchema
)
from common.response.response_chema import (
    ResponseModel,
    response_base
)
from common.response.response_code import CustomResponseCode
from core.mongo_db import MongoDB

router = APIRouter()


@router.get(
    '/',
    summary='Получить все из MongoDB',
    description="Получаем данные из MongoDB в виде коллекции",
)
async def get_all_from_mongo(db: MongoDB, filter: MongoPaginateSchema = Depends()) -> ResponseModel:
    """returns a set of documents belonging to page number `page_num`
    where size of each page is `page_size`.
    """
    # Calculate number of documents to skip
    skips = filter.page_size * (filter.page_num - 1)

    # Skip and limit
    cursor = (
        db["users"].
        find(limit=100).
        sort("_id", pymongo.ASCENDING).
        skip(skips).
        limit(filter.page_size)
    )

    # Return documents
    users = [x for x in cursor]

    return await response_base.success(
        data=users
    )
