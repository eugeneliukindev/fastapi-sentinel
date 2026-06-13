from typing import Literal

from pydantic import BaseModel, EmailStr


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    type: Literal["Bearer"] = "Bearer"


class LogoutSchema(BaseModel):
    refresh_token: str
