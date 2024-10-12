from sqlalchemy.ext.asyncio import AsyncSession

from api.permission.repository import permission_repository
from api.permission.schemas import (
    PermissionSchema
)


class PermissionService:
    @staticmethod
    async def get_permissions(db: AsyncSession):
        permissions = await permission_repository.get_permissions(db)
        # return [Permission(permission) for permission in permissions]
        return [PermissionSchema(**permission.__dict__) for permission in permissions]

    @staticmethod
    async def get_permission_by_id(
            db: AsyncSession,
            permission_id: int
    ):
        permission = await permission_repository.get_permission_by_id(permission_id, db)
        if permission is None:
            return None
        return PermissionSchema(**permission.__dict__)

    @staticmethod
    async def create_permission(data: dict, db: AsyncSession):
        permission = await permission_repository.create_permission(data, db)
        if permission is None:
            return None
        return PermissionSchema(**permission.__dict__)

    @staticmethod
    async def update_permission(db: AsyncSession):
        pass

    @staticmethod
    async def delete_permission(permission_id: int, db: AsyncSession) -> bool:
        return await permission_repository.delete_permission(permission_id, db)


permission_service = PermissionService()
