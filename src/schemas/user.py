from pydantic import BaseModel, ConfigDict, EmailStr

from src.schemas.rbac import RoleReadS
from src.schemas.rbac.role import RoleReadWithPermissionsS


class UserCreateS(BaseModel):
    email: EmailStr
    password: str


class UserUpdateS(BaseModel):
    email: str | None = None


class UserReadS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class UserReadWithRolesS(UserReadS):
    roles: list[RoleReadS]

    def has_role(self, *names: str) -> bool:
        role_names = {role.name for role in self.roles}
        return all(name in role_names for name in names)


class UserReadWithRolesAndPermissionsS(UserReadWithRolesS):
    roles: list[RoleReadWithPermissionsS]

    def has_permission(self, *names: str) -> bool:
        permissions = {p.name for role in self.roles for p in role.permissions}
        return all(name in permissions for name in names)
