from sqlalchemy import exists, select

from src.dto.token_blacklist import TokenBlacklistInsert
from src.models.token_blacklist import TokenBlacklist
from src.repo.base import BaseRepository


class TokenBlacklistRepository(BaseRepository[TokenBlacklist, TokenBlacklistInsert, TokenBlacklistInsert]):
    model = TokenBlacklist

    async def is_blacklisted(self, jti: str) -> bool:
        result = await self._session.scalar(select(exists().where(TokenBlacklist.jti == jti)))
        return bool(result)
