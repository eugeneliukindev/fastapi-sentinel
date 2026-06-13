from pydantic import BaseModel


class PermissionInsertDTO(BaseModel):
    name: str
    description: str = ""
