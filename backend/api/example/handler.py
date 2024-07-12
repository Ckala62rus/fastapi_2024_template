from typing import Annotated

from fastapi import APIRouter, Request, Body, status, Depends

from api.example.schemas import (
    HelloSchemaCreated,
    HelloSchemaRetrieve,
    HelloSchemaUpdate
)
from common.response.response_chema import response_base, ResponseModel
from common.response.response_code import CustomResponseCode
from common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.get(
    "/hello",
    summary="hello world endpoint swagger",
    description="hello world endpoint description swagger",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel, # custom pydantic model for 200 response
            "description": "Ok Response",
        },
    },
)
async def hello_world(request: Request) -> ResponseModel:
    return await response_base.success(
        data={
            "id": 1,
            "name": "some name",
            "age": "some age",
            "phone": "88005553535",
        }
    )


@router.get(
    "/hello/{hello_id}",
    summary="get hello world by id method GET",
    description="get hello world by id",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel, # custom pydantic model for 200 response
            "description": "Ok Response",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ResponseModel,  # custom pydantic model for 201 response
            "description": "Entity not found",
        },
    },
)
async def hello_world_get_by_id(
    request: Request,
    hello: HelloSchemaRetrieve = Depends(),
) -> ResponseModel:
    if hello.id == 7:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=f"Not Found with id {hello.id}"
        )
    return await response_base.success(
        data={
            "id": hello.id,
            "name": "some name",
            "age": "some age",
            "phone": "88005553535",
        }
    )


@router.post(
    "/hello",
    summary="hello world some POST params",
    description="some POST params endpoint description swagger",
    responses={
        status.HTTP_201_CREATED: {
            "model": ResponseModel,  # custom pydantic model for 201 response
            "description": "Entity was created",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ResponseModel,  # custom pydantic model for 201 response
            "description": "Creates with error",
        },
    },
)
async def hello_world_post(
    request: Request,
    hello: Annotated[HelloSchemaCreated, Body()]
):
    return {
        "name": hello.name,
        "age": 25,
        "phone": "88005553535",
    }


@router.put(
    '/hello/{hello_id}',
    summary="hello world example PUT update",
    description="Update method PUT example swagger. (for the test with id 7 not found)",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel, # custom pydantic model for 200 response
            "description": "Entity was updated",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ResponseModel,  # custom pydantic model for 201 response
            "description": "Entity not found",
        },
    },
)
async def hello_world_update_by_id(
    hello_id: int,
    request: Request,
    hello: Annotated[HelloSchemaUpdate, Body()]
) -> ResponseModel:
    if hello_id == 7:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=f"Not Found with id {hello_id}"
        )

    return await response_base.success(
        data={
            "id": hello_id,
            "name": hello.name,
            "age": hello.age,
            "phone": hello.phone,
        }
    )


@router.delete(
    '/hello/{hello_id}',
    summary="hello world example DELETE delete",
    description="Delete method DELETE example swagger. (for the test with id 7 not found)",
)
async def hello_world_delete_by_id(
    hello_id: int,
) -> ResponseModel:
    if hello_id == 7:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data={
                "id": hello_id,
            }
        )
    return await response_base.success(
        data={
            "id": hello_id,
        }
    )
