from datetime import UTC, datetime

from src.core.uow import UnitOfWork
from src.dto import TokenBlacklistInsert, TokenPayload


class TokenBlacklistService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def blacklist_token(self, payload: TokenPayload) -> None:
        await self._uow.token_blacklist.add(
            TokenBlacklistInsert(
                jti=payload.jti,
                expires_at=datetime.fromtimestamp(payload.exp, tz=UTC),
            )
        )

    async def is_blacklisted(self, jti: str) -> bool:
        return await self._uow.token_blacklist.is_blacklisted(jti)
