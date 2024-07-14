from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, unique=True)
    date = Column(DateTime, nullable=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str | None] = mapped_column(String(255))

    class ConfigDict:
        from_attributes = True
