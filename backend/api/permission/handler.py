from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

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
            "description": "Permission form databbase",
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
