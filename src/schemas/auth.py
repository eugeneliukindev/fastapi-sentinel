from typing import Literal

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    type: Literal["Bearer"] = "Bearer"
