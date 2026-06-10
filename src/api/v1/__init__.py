from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.rbac import router as rbac_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(rbac_router)
