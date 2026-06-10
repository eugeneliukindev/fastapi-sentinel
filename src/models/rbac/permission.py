from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.rbac.roles_permissions import roles_permissions_association_table

if TYPE_CHECKING:
    from src.models.rbac.role import Role


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    roles: Mapped[set[Role]] = relationship(
        "Role", secondary=roles_permissions_association_table, back_populates="permissions"
    )
