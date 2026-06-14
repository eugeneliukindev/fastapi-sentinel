from datetime import UTC, datetime

from src.core.uow import UnitOfWork
from src.dto import TokenBlacklistInsertDTO, TokenPayloadDTO


class TokenBlacklistService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def blacklist_token(self, payload: TokenPayloadDTO) -> None:
        self._uow.token_blacklist.add(
            TokenBlacklistInsertDTO(
                jti=payload.jti,
                expires_at=datetime.fromtimestamp(payload.exp, tz=UTC),
            )
        )

    async def is_blacklisted(self, jti: str) -> bool:
        return await self._uow.token_blacklist.is_blacklisted(jti)
