from pydantic import BaseModel, ConfigDict

from src.schemas.rbac import PermissionReadS


class RoleReadS(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    name: str
    description: str


class RoleReadWithPermissionsS(RoleReadS):
    permissions: list[PermissionReadS]
