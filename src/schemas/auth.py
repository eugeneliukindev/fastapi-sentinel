from typing import Literal

from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_key: str
    type: Literal["Bearer"] = "Bearer"


class TokenResponse(AccessTokenResponse):
    refresh_key: str
