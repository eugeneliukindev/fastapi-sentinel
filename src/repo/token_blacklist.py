from sqlalchemy import exists, select

from src.dto.token_blacklist import TokenBlacklistInsertDTO
from src.models.token_blacklist import TokenBlacklistOrm
from src.repo.base import BaseRepository


class TokenBlacklistRepository(BaseRepository[TokenBlacklistOrm, TokenBlacklistInsertDTO, TokenBlacklistInsertDTO]):
    model = TokenBlacklistOrm

    async def is_blacklisted(self, jti: str) -> bool:
        stmt = select(exists().where(TokenBlacklistOrm.jti == jti))
        result = await self._session.scalar(stmt)
        return bool(result)
