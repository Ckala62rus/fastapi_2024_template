from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Body

from common.response.response_chema import ResponseModel, response_base
from middleware.auth_jwt_middleware import JWTBearer
from task.service.task_service import task_service

router = APIRouter()


@router.get(
    '/',
    summary='Получить все исполняемые модули задач',
    dependencies=[Depends(JWTBearer())]
)
async def get_all_tasks() -> ResponseModel:
    tasks = task_service.get_list()
    return await response_base.success(data=tasks)


@router.post(
    '/{name}',
    summary='выполнять задание',
)
async def run_task(
    name: Annotated[str, Path(description='Название задачи')],
    args: Annotated[list | None, Body(description='Позиционные параметры целевой функции')] = None,
    kwargs: Annotated[dict | None, Body(description='Параметры ключевого слова целевой функции')] = None,
) -> ResponseModel:
    task = task_service.run(name=name, args=args, kwargs=kwargs)
    return await response_base.success(data=task.task_id)
    # return task
