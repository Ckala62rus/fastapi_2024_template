from http.client import HTTPException
from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends
)
from starlette import status
from starlette.requests import Request

from api.user.schemas import (
    AuthSchemaBase,
    AuthSchemaCreate,
    AuthLoginSchema
)
from api.user.service import UserService
from common.response.response_chema import response_base
from common.response.response_code import CustomResponseCode
from core.db import async_db_session
from middleware.auth_jwt_middleware import JWTBearer

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
        async with async_db_session.begin() as db:
            created_user = await UserService().registration(credentials, db)
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


@router.post(
    "/login",
    summary="Login",
    description="Enter login credentials and return access token",
)
async def login(credentials: Annotated[AuthLoginSchema, Body()]):
    try:
        async with async_db_session.begin() as db:
            result = await UserService().login(credentials, db)
        return await response_base.success(
        res=CustomResponseCode.HTTP_200,
        data=result
    )
    except HTTPException as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Error /login route. {e}"
        )


@router.get(
    '/me',
    summary="Me",
    description="Return model of current user",
    dependencies=[Depends(JWTBearer())],
)
async def me(request: Request):
    try:
        async with async_db_session.begin() as db:
            user = await UserService.me(request.user_id, db)
            return await response_base.success(
                res=CustomResponseCode.HTTP_200,
                data=user
            )
    except HTTPException as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Error /login route. {e}"
        )
