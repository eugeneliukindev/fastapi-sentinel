from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.rbac.role import Role


class User(Base):
    __tablename__ = "users"
    __repr_exclude__: ClassVar[frozenset[str]] = frozenset({"hashed_password"})

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    role: Mapped[Role] = relationship("Role", back_populates="users")
