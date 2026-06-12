from pydantic import BaseModel


class UserInsertDTO(BaseModel):
    email: str
    hashed_password: str


class UserUpdateDTO(BaseModel):
    email: str | None = None
