from pydantic import BaseModel


class UserInsert(BaseModel):
    username: str
    hashed_password: str
    role_id: int


class UserUpdate(BaseModel):
    username: str | None = None
