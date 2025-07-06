from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette import status
from loguru import logger

from api.permission.schemas import PermissionCreateSchema
from api.permission.service import PermissionService
from common.response.response_chema import ResponseModel, response_base
from common.response.response_code import CustomResponseCode
from core.db import get_db
from models.permission import Permission
from middleware.auth_jwt_middleware import JWTBearer

router = APIRouter()


@router.get(
    "/",
    summary="Get all permissions",
    description="Get all permissions from database",
    dependencies=[Depends(JWTBearer())],
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
    try:
        permissions = await PermissionService.get_permissions(db)
        logger.info(f"Retrieved {len(permissions) if permissions else 0} permissions")
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=permissions
        )
    except Exception as e:
        logger.error(f"Error retrieving permissions: {e}")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_500,
            data=f"Failed to retrieve permissions: {e}"
        )


@router.get(
    "/{permission_id}",
    summary="Get permission by id",
    description="Get permission by id",
    dependencies=[Depends(JWTBearer())],
)
async def get_permission_by_id(
        permission_id: int,
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        permission = await PermissionService.get_permission_by_id(db, permission_id)
        if permission is None:
            logger.warning(f"Permission with ID {permission_id} not found")
            return await response_base.fail(
                res=CustomResponseCode.HTTP_404,
                data=f"Permission with ID {permission_id} not found"
            )
        logger.info(f"Retrieved permission: {permission_id}")
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=permission
        )
    except Exception as e:
        logger.error(f"Error retrieving permission {permission_id}: {e}")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_500,
            data=f"Failed to retrieve permission: {e}"
        )


@router.post(
    '/',
    summary="Create permission",
    description="Create permission",
    dependencies=[Depends(JWTBearer())],
)
async def create_permission(
        permission_create: PermissionCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    try:
        permission = await PermissionService.create_permission(
            permission_create.model_dump(),
            db
        )
        logger.info(f"Created permission: {permission_create.name}")
        return await response_base.success(
            res=CustomResponseCode.HTTP_201,
            data=permission
        )
    except IntegrityError as e:
        logger.warning(f"Permission with name '{permission_create.name}' already exists")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Permission with name '{permission_create.name}' already exists"
        )
    except Exception as e:
        logger.error(f"Error creating permission {permission_create.name}: {e}")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Failed to create permission: {e}"
        )


@router.delete(
    '/{permission_id}',
    summary="Delete permission",
    description="Delete permission",
    dependencies=[Depends(JWTBearer())],
)
async def delete_permission(
        permission_id: int,
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        permission = await PermissionService.delete_permission(permission_id, db)
        if permission is False:
            logger.warning(f"Permission with ID {permission_id} not found for deletion")
            return await response_base.fail(
                res=CustomResponseCode.HTTP_404,
                data=f"Permission with ID {permission_id} not found"
            )
        logger.info(f"Deleted permission: {permission_id}")
        return await response_base.success(
            res=CustomResponseCode.HTTP_204,
            data=None
        )
    except Exception as e:
        logger.error(f"Error deleting permission {permission_id}: {e}")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_500,
            data=f"Failed to delete permission: {e}"
        )
