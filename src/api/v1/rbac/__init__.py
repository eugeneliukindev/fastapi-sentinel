from fastapi import APIRouter, Depends

from src.api.dependencies.auth import require_role
from src.api.v1.rbac.permissions import router as permissions_router
from src.api.v1.rbac.roles import router as roles_router
from src.enums import RoleEnum

router = APIRouter(
    prefix="/rbac",
    dependencies=[Depends(require_role(RoleEnum.ADMIN))],
)
router.include_router(roles_router)
router.include_router(permissions_router)
