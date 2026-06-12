from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseOrm

if TYPE_CHECKING:
    from src.models import RoleOrm


class UserOrm(BaseOrm):
    __tablename__ = "users"
    __repr_exclude__: ClassVar[frozenset[str]] = frozenset({"hashed_password"})

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    roles: Mapped[list[RoleOrm]] = relationship(
        "RoleOrm",
        secondary="user_roles",
        back_populates="users",
    )
