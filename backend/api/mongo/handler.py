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


@router.post(
    '/',
    summary='Добавить что то в MongoDB',
    description="Создание записи в MongoDB",
)
async def create_in_mongo(db: MongoDB) -> ResponseModel:
    user = db["users"].insert_one({
        "_id": randint(1, 1000), # here primary key from Database (PostgresSQL / MySql)
        "name": "admin",
        "email": "admin@mail.ru",
        "password": "<PASSWORD>",
        "is_active": True,
    })
    result = db["users"].find_one(
        {"_id": user.inserted_id}
    )
    return await response_base.success(
        data=result
    )


@router.get(
    '/{id}',
    summary='Получить конкретную запись по id из MongoDB',
    description="Получаем данные из MongoDB в виде коллекции",
)
async def get_by_id_from_mongo(id: int, db: MongoDB) -> ResponseModel:
    user = db["users"].find_one({"_id": id})
    if user is None:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=f"Not Found with id {id}"
        )
    return await response_base.success(
        data=user
    )


@router.put(
    '/{id}',
    summary='Обновление данных по id MongoDB',
    description="Обновляем данные в MongoDB и возвращаем результат обновленной модели",
)
async def update_by_id_from_mongo(
    id: int,
    db: MongoDB,
    data: UpdateDateMongoDBSchema
) -> ResponseModel:
    data_dict = {k: v for k, v in data.dict().items() if v is not None}
    if len(data_dict) >= 1:
        update_result = db["users"].update_one(
            {"_id": id}, {"$set": data_dict}
        )

        if update_result.modified_count == 0:
            return await response_base.fail(
                res=CustomResponseCode.HTTP_200,
                data=f"Data with id {id} wasn't updated"
            )
    entity = db["users"].find_one({"_id": id})
    if entity is None:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=f"Not Found with id {id}"
        )
    return await response_base.success(
        data=entity
    )


@router.delete(
    "/{id}",
    summary="Удаление данных по id",
    description="Удаление данных из MongoDB по id"
)
async def delete_by_id_from_mongo(
    id: int,
    db: MongoDB
) -> ResponseModel:
    delete_result = db["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 0:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=f"Entity with id {id} wasn't deleted"
        )

    return await response_base.success(
        res=CustomResponseCode.HTTP_200,
        data={"message": f"Entity with id {id} was deleted"}
    )
