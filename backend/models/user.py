from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship
)

from common.model import (
    Base,
    id_key
)
from models.permission import Permission


class User(Base):
    __tablename__ = "users"

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='Ник')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str | None] = mapped_column(String(255))
    refresh_token: Mapped[str | None] = mapped_column(String(255))
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='Админ')
    is_staff: Mapped[bool] = mapped_column(default=False, comment='Фоновое управление')

    permissions: Mapped[list["Permission"]] = relationship(
        # noqa: F821
        init=False,
        secondary="users_permissions",
        back_populates='users'
    )
