from pydantic import BaseModel


class PermissionInsert(BaseModel):
    name: str


class PermissionUpdate(BaseModel):
    name: str | None = None
