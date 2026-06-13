from pydantic import BaseModel

from src.dto.permission import PermissionInsertDTO
from src.models.permission import PermissionOrm
from src.repo.base import BaseRepository


class PermissionRepository(BaseRepository[PermissionOrm, PermissionInsertDTO, BaseModel]):
    model = PermissionOrm
