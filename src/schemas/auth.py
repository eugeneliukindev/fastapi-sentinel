from typing import Literal

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_key: str
    refresh_key: str
    type: Literal["Bearer"] = "Bearer"
