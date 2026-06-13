from pydantic import BaseModel
from sqlalchemy import select

from src.dto.role import RoleInsertDTO
from src.models.role import RoleOrm
from src.repo.base import BaseRepository


class RoleRepository(BaseRepository[RoleOrm, RoleInsertDTO, BaseModel]):
    model = RoleOrm

    async def get_by_name(self, name: str) -> RoleOrm | None:
        return await self._session.scalar(select(RoleOrm).where(RoleOrm.name == name))  # type: ignore[no-any-return]
