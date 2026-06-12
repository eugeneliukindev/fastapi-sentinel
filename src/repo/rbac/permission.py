from pydantic import BaseModel

from src.dto.rbac.permission import PermissionInsertDTO
from src.models.rbac.permission import PermissionOrm
from src.repo.base import BaseRepository


class PermissionRepository(BaseRepository[PermissionOrm, PermissionInsertDTO, BaseModel]):
    model = PermissionOrm
