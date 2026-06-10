from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.rbac.roles_permissions import roles_permissions_association_table

if TYPE_CHECKING:
    from src.models.rbac.permission import Permission
    from src.models.user import User


class RoleEnum(StrEnum):
    ADMIN = "admin"
    USER = "user"


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[RoleEnum] = mapped_column(unique=True, nullable=False)

    permissions: Mapped[set[Permission]] = relationship(
        "Permission", secondary=roles_permissions_association_table, back_populates="roles"
    )
    users: Mapped[list[User]] = relationship("User", back_populates="role")
