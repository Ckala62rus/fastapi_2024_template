from sqlalchemy.ext.asyncio import AsyncSession

from api.permission.repository import permission_repository
from api.permission.schemas import PermissionAllSchema, PermissionCreateSchema


class PermissionService:
    @staticmethod
    async def get_permissions(db: AsyncSession):
        permissions = await permission_repository.get_permissions(db)
        return [PermissionAllSchema(**permission) for permission in permissions]

    @staticmethod
    async def get_permission_by_id(
        db: AsyncSession,
        permission_id: int
    ):
        permission = await permission_repository.get_permission_by_id(permission_id, db)
        if permission is None:
            return None
        return PermissionAllSchema(**permission)

    @staticmethod
    async def create_permission(db: AsyncSession):
        pass

    @staticmethod
    async def update_permission(db: AsyncSession):
        pass

    @staticmethod
    async def delete_permission(db: AsyncSession):
        pass


permission_service = PermissionService()
