from typing import Literal

from pydantic import BaseModel, EmailStr


class LoginRequestS(BaseModel):
    email: EmailStr
    password: str


class TokenResponseS(BaseModel):
    access_token: str
    refresh_token: str
    type: Literal["Bearer"] = "Bearer"
