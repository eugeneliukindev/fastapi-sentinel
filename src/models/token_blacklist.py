from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseOrm


class TokenBlacklistOrm(BaseOrm):
    __tablename__ = "token_blacklist"

    jti: Mapped[str] = mapped_column(primary_key=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
