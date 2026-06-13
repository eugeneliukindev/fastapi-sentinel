from pydantic import BaseModel, ConfigDict, EmailStr

from src.schemas.common import PartialSchemaMixin
from src.schemas.role import RoleReadSchema, RoleReadWithPermissionsSchema


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    email: EmailStr


class UserPartialUpdateSchema(UserUpdateSchema, PartialSchemaMixin):
    pass


class UserChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str


class UserResetPasswordSchema(BaseModel):
    new_password: str


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class UserReadWithRolesSchema(UserReadSchema):
    roles: list[RoleReadSchema]

    def has_role(self, *names: str) -> bool:
        role_names = {role.name for role in self.roles}
        return all(name in role_names for name in names)

    def has_any_role(self, *names: str) -> bool:
        role_names = {role.name for role in self.roles}
        return any(name in role_names for name in names)


class UserReadWithRolesAndPermissionsSchema(UserReadWithRolesSchema):
    roles: list[RoleReadWithPermissionsSchema]  # type: ignore[assignment]

    def has_permission(self, *names: str) -> bool:
        permissions = {p.name for role in self.roles for p in role.permissions}
        return all(name in permissions for name in names)

    def has_any_permission(self, *names: str) -> bool:
        permissions = {p.name for role in self.roles for p in role.permissions}
        return any(name in permissions for name in names)
