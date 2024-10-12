from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from common.model import Base, id_key
from models.user_permission import UserPermission


class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='Название разрешения')

    users: Mapped[list["User"]] = relationship(
        # noqa: F821
        init=False,
        secondary="users_permissions",
        back_populates='permissions'
    )
