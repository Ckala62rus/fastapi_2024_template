from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.permission.schemas import PermissionCreateSchema
from api.permission.service import PermissionService
from common.response.response_chema import ResponseModel, response_base
from common.response.response_code import CustomResponseCode
from core.db import get_db
from models.permission import Permission

router = APIRouter()


@router.get(
    "/",
    summary="Get all permissions",
    description="Get all permissions from database",
    responses={
        status.HTTP_200_OK: {
            "model": Permission,
            "description": "Permission form database",
        },
    },
)
async def get_permissions(
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    permissions = await PermissionService.get_permissions(db)
    return await response_base.success(
        res=CustomResponseCode.HTTP_200,
        data=permissions
    )


@router.get(
    "/{permission_id}",
    summary="Get permission by id",
    description="Get permission by id",
)
async def get_permission_by_id(
        permission_id: int,
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    permission = await PermissionService.get_permission_by_id(db, permission_id)
    if permission is None:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=None
        )
    return await response_base.success(
        res=CustomResponseCode.HTTP_200,
        data=permission
    )


@router.post(
    '/',
    summary="Create permission",
    description="Create permission",
)
async def create_permission(
        permission_create: PermissionCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    permission = await PermissionService.create_permission(
        permission_create.model_dump(),
        db
    )
    return await response_base.success(
        res=CustomResponseCode.HTTP_201,
        data=permission
    )


@router.delete(
    '/{permission_id}',
    summary="Delete permission",
    description="Delete permission",
)
async def delete_permission(
        permission_id: int,
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    permission = await PermissionService.delete_permission(permission_id, db)
    if permission is False:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_404,
            data=None
        )
    return await response_base.success(
        res=CustomResponseCode.HTTP_204,
        data=None
    )
