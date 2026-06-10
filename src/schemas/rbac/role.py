from pydantic import BaseModel, ConfigDict

from src.models.rbac.role import RoleEnum
from src.schemas.rbac.permission import PermissionRead


class RoleCreate(BaseModel):
    name: RoleEnum


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: RoleEnum
    permissions: set[PermissionRead]
