from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Body
from starlette import status

from api.user.schemas import AuthSchemaBase, AuthSchemaCreate
from api.user.service import UserService
from common.response.response_chema import response_base
from common.response.response_code import CustomResponseCode

router = APIRouter()

@router.post(
    "/registration",
    summary="Registration user",
    description="Registration user and return user model",
    responses={
        status.HTTP_201_CREATED: {
            "model": AuthSchemaCreate,  # custom pydantic model for 201 response
            "description": "Entity was created",
        },
    },
)
async def registration(credentials: Annotated[AuthSchemaBase, Body()]):
    try:
        created_user = await UserService().registration(credentials)
    except HTTPException as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"User with {credentials.email} if exists"
        )
    except Exception as e:
        return await response_base.fail(data=str(e))
    return await response_base.success(
        res=CustomResponseCode.HTTP_201,
        data=created_user
    )


async def login():
    pass

