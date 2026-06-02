from sqlalchemy import select

from src.dto.user import UserInsert, UserUpdate
from src.models.user import User
from src.repo.base import BaseRepository


class UserRepository(BaseRepository[User, UserInsert, UserUpdate]):
    model = User

    async def get_by_username(self, username: str) -> User | None:
        return await self._session.scalar(select(User).where(User.username == username))
