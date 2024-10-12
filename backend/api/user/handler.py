from http.client import HTTPException
from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends
)
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from api.user.schemas import (
    AuthSchemaBase,
    AuthSchemaCreate,
    AuthLoginSchema,
    PaginationSchema,
)
from api.user.service import (
    UserService,
    user_service
)
from common.response.response_chema import (
    response_base,
    ResponseModel
)
from common.response.response_code import CustomResponseCode
from core.db import get_db
# from middleware.PermissionChecker import PermissionChecker
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
async def registration(
        credentials: Annotated[AuthSchemaBase, Body()],
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
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
async def login(
        credentials: Annotated[AuthLoginSchema, Body()],
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        result = await UserService().login(credentials, db)
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=result.model_dump()
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
    dependencies=[
        Depends(JWTBearer()),
        # Depends(PermissionChecker([]))
    ],
)
async def me(
        request: Request,
        db: AsyncSession = Depends(get_db),
        # authorize: bool = Depends(PermissionChecker(required_permissions=['items:read', ]))
) -> ResponseModel:
    try:
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


@router.post(
    '/logout',
    summary="Logout",
    description="Logout",
    dependencies=[Depends(JWTBearer())],
)
async def logout(request: Request) -> ResponseModel:
    try:
        await user_service.logout(request=request)
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data={"logout"}
        )
    except HTTPException as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Error /login route. {e}"
        )


@router.post(
    '/token/refresh',
    summary="Refresh",
    description="Refresh token and return new access_token and refresh token",
    dependencies=[Depends(JWTBearer())],
)
async def token_refresh(
        request: Request,
        refresh_token: Annotated[str, Query(...)],
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        result = await user_service.token_refresh(request=request, refresh_token=refresh_token, db=db)
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=result.model_dump()
        )
    except HTTPException as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Error /login route. {e}"
        )


@router.get(
    '/users',
    summary="Users",
    description="Return all users",
)
async def get_all_users(
    pagination: PaginationSchema = Depends(),
    db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    users = await UserService().get_all_users(
        db,
        pagination.limit,
        pagination.page,
    )
    return await response_base.success(
        res=CustomResponseCode.HTTP_200,
        data=users
    )
