from pydantic import BaseModel, ConfigDict


class PermissionReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    name: str
    description: str
