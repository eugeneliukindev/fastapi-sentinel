from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseOrm
from src.models.role import RoleOrm

if TYPE_CHECKING:
    pass


class PermissionOrm(BaseOrm):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    roles: Mapped[set[RoleOrm]] = relationship(
        "RoleOrm",
        secondary="role_permissions",
        back_populates="permissions",
    )
