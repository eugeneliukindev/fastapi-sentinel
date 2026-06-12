from datetime import datetime

from pydantic import BaseModel


class TokenBlacklistInsertDTO(BaseModel):
    jti: str
    expires_at: datetime
