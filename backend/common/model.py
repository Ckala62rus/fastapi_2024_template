from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column, MappedAsDataclass, Mapped, DeclarativeBase, declared_attr

from utils.timezone import timezone

id_key = Annotated[
    int, mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
        sort_order=-999,
        comment='Primary key'
    )
]

class UserMixin(MappedAsDataclass):
    """Mixin для добавления таблицам данных о том кто создавал и обновлял"""

    create_user: Mapped[int] = mapped_column(
        sort_order=998,
        comment='Пользователь, который создал запись'
    )
    update_user: Mapped[int | None] = mapped_column(
        init=False,
        default=None,
        sort_order=998,
        comment='Пользователь обновивший запись'
    )


class DateTimeMixin(MappedAsDataclass):
    """Mixin для добавления даты создания и обновления записи"""

    created_time: Mapped[datetime] = mapped_column(
        init=False,
        default_factory=timezone.now,
        sort_order=999,
        comment='Время создания'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        init=False,
        onupdate=timezone.now,
        sort_order=999,
        comment='Время обновления'
    )


class MappedBase(DeclarativeBase):
    """
    DeclarativeBase

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    DeclarativeBase

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """  # noqa: E501

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """
    Mixin для базовых классов моделей
    """  # noqa: E501

    __abstract__ = True
