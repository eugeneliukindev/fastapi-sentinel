from pydantic import BaseModel

from src.models.rbac.role import RoleEnum


class RoleInsert(BaseModel):
    name: RoleEnum


class RoleUpdate(BaseModel):
    name: RoleEnum | None = None
