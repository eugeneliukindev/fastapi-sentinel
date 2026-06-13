from pydantic import BaseModel, ConfigDict

from src.schemas.permission import PermissionReadSchema


class RoleReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    name: str
    description: str


class RoleReadWithPermissionsSchema(RoleReadSchema):
    permissions: list[PermissionReadSchema]
