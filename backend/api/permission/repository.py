from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.permission import Permission


class PermissionRepository:
    """
    Get all permission from database

    :param db: AsyncSession
    :return:
    """
    @staticmethod
    async def get_permissions(db: AsyncSession):
        query = select(Permission).options(selectinload(Permission.users))
        result = await db.execute(query)
        return result.scalars().all()

    """
    Get single permission by id
    
    :param permission_id: int
    :param db: AsyncSession
    :return: Permission
    """
    @staticmethod
    async def get_permission_by_id(
            permission_id: int,
            db: AsyncSession
    ) -> Permission | None:
        query = select(Permission).where(Permission.id == permission_id)
        result = await db.execute(query)
        permission = result.scalar()
        if permission is None:
            return None
        return permission

    """
    Create a new permission
    
    :param data: dict
    :param db: AsyncSession
    :return: Permission
    """
    @staticmethod
    async def create_permission(
            data: dict,
            db: AsyncSession
    ) -> Permission:
        permission = Permission(**data)
        db.add(permission)
        await db.commit()
        return permission

    @staticmethod
    async def update_permission(permission_id: int, data: dict):
        pass

    """
    Delete single permission by id

    :param permission_id: int
    :param db: AsyncSession
    :return: Bool
    """
    @staticmethod
    async def delete_permission(permission_id: int, db: AsyncSession) -> bool:
        stmt = await db.execute(select(Permission).where(Permission.id == permission_id))
        obj = stmt.scalar()
        if obj is None:
            return False
        await db.delete(obj)
        await db.commit()
        return True


permission_repository = PermissionRepository()
