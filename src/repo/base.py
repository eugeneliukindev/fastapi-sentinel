from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete, inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import BaseOrm


class BaseRepository[ModelT: BaseOrm, InsertT: BaseModel, UpdateT: BaseModel]:
    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: Any) -> ModelT | None:
        return await self._session.get(self.model, entity_id)

    async def get_all(self) -> list[ModelT]:
        result = await self._session.execute(select(self.model))
        return list(result.scalars().all())

    async def add(self, data: InsertT) -> ModelT:
        entity = self.model(**data.model_dump())
        self._session.add(entity)
        await self._session.flush()
        return entity

    async def update(self, entity_id: Any, data: UpdateT) -> ModelT | None:
        pk = inspect(self.model).mapper.primary_key[0]
        stmt = (
            update(self.model)
            .where(pk == entity_id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, entity_id: Any) -> ModelT | None:
        pk = inspect(self.model).mapper.primary_key[0]
        stmt = delete(self.model).where(pk == entity_id).returning(self.model)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
