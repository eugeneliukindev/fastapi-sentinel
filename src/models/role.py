from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseOrm
from src.models.user import UserOrm

if TYPE_CHECKING:
    from .permission import PermissionOrm


class RoleOrm(BaseOrm):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    permissions: Mapped[set[PermissionOrm]] = relationship(
        "PermissionOrm",
        secondary="role_permissions",
        back_populates="roles",
    )
    users: Mapped[list[UserOrm]] = relationship(
        "UserOrm",
        secondary="user_roles",
        back_populates="roles",
    )
