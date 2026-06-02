from datetime import datetime

from pydantic import BaseModel


class TokenBlacklistInsert(BaseModel):
    jti: str
    expires_at: datetime
