from pydantic import BaseModel, ConfigDict

from src.schemas.rbac.role import RoleRead


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: RoleRead
