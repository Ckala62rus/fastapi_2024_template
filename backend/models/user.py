from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from common.model import Base, id_key


# from core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='Ник')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str | None] = mapped_column(String(255))
    refresh_token: Mapped[str | None] = mapped_column(String(255))
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='Админ')
    is_staff: Mapped[bool] = mapped_column(default=False, comment='Фоновое управление')
