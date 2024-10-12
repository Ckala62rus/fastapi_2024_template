from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from common.model import id_key, Base


class UserPermission(Base):
    __tablename__ = 'users_permissions'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )
