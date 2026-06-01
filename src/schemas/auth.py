from typing import Literal

from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str
    type: Literal["Bearer"] = "Bearer"


class TokenResponse(AccessTokenResponse):
    refresh_token: str
