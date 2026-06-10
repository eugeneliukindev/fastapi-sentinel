from sqlalchemy import Column, ForeignKey, Integer, Table

from src.models import Base

roles_permissions_association_table = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)
