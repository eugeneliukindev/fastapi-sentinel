from pydantic import BaseModel


class RoleInsertDTO(BaseModel):
    name: str
    description: str = ""
