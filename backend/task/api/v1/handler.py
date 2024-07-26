from pathlib import Path
from random import randint
from typing import Annotated

from fastapi import APIRouter, Depends, Body

from common.exception.errors import NotFoundError
from common.response.response_chema import ResponseModel, response_base
from common.response.response_code import CustomResponseCode
from core.mongo_db import MongoDB
from middleware.auth_jwt_middleware import JWTBearer
from task.service.task_service import task_service

router = APIRouter()


@router.get(
    '/',
    summary='Получить все исполняемые модули задач',
    # dependencies=[Depends(JWTBearer())]
)
async def get_all_tasks() -> ResponseModel:
    tasks = task_service.get_list()
    return await response_base.success(data=tasks)


@router.get(
    '/current',
    summary='Получите текущую выполняемую задачу',
    # dependencies=[Depends(JWTBearer())]
)
async def get_current_task() -> ResponseModel:
    task = task_service.get()
    return await response_base.success(data=task)


@router.get(
    '/{uid}/status',
    summary='Получить статус задачи',
    # dependencies=[Depends(JWTBearer())]
)
async def get_task_status(
    uid: Annotated[str, Path(description='Стутус задачи по ID')]
) -> ResponseModel:
    try:
        status = task_service.get_status(uid)
        return await response_base.success(data=status)
    except NotFoundError as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=f"Task with id {uid} not found"
        )


@router.get(
    '/{uid}',
    summary='Получение результатов выполнения задачи',
    # dependencies=[Depends(JWTBearer())]
)
async def get_task_result(uid: Annotated[str, Path(description='Идентификатор задачи ID')]) -> ResponseModel:
    task = task_service.get_result(uid)
    return await response_base.success(data=task.result)


@router.post(
    '/{name}',
    summary='выполнять задание',
)
async def run_task(
    name: Annotated[str, Path(description='Название задачи')],
    message: str
    # args: Annotated[list | None, Body(description='Позиционные параметры целевой функции')] = None,
    # kwargs: Annotated[dict | None, Body(description='Параметры ключевого слова целевой функции')] = None,
) -> ResponseModel:
    # task = task_service.run(name=name, args=args, kwargs={"msg": message})
    task = task_service.run(name=name, kwargs={"msg": message})
    return await response_base.success(data=task.task_id)


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

