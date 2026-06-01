from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


class BaseRepository[ModelT: Base]:
    """Generic repository over a single ORM model, operating on an injected session.

    Subclasses set the concrete model:  `class UserRepository(BaseRepository[User]): model = User`.
    """

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: int) -> ModelT | None:
        return await self._session.get(self.model, entity_id)

    async def add(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        await self._session.flush()  # populates server-side defaults (e.g. id) without committing
        return entity

    async def delete(self, entity: ModelT) -> None:
        await self._session.delete(entity)
