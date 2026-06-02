from pydantic import BaseModel


class UserInsert(BaseModel):
    username: str
    hashed_password: str


class UserUpdate(BaseModel):
    username: str | None = None
