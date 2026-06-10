import re

from pydantic import BaseModel, ConfigDict, field_validator

from src.exceptions.rbac import InvalidPermissionFormatError

_PERMISSION_FORMAT = re.compile(r"^[a-z_]+:[a-z_]+$")


class PermissionCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_format(cls, v: str) -> str:
        if not _PERMISSION_FORMAT.match(v):
            raise InvalidPermissionFormatError
        return v


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    name: str
