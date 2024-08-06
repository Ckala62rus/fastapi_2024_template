from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.permission import Permission


class PermissionRepository:
    @staticmethod
    async def get_permissions(db: AsyncSession):
        query = select(Permission)
        result = await db.execute(query)
        return result

    @staticmethod
    async def get_permission_by_id(permission_id: int):
        pass

    @staticmethod
    async def create_permission(data: dict):
        pass

    @staticmethod
    async def update_permission(permission_id: int, data: dict):
        pass

    @staticmethod
    async def delete_permission(permission_id: int):
        pass


permission_repository = PermissionRepository()
