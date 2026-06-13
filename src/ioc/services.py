from dishka import Provider, Scope, provide

from src.services.auth.blacklist import TokenBlacklistService
from src.services.auth.service import AuthService
from src.services.permission import PermissionService
from src.services.role import RoleService
from src.services.user import UserService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    token_blacklist_service = provide(TokenBlacklistService)
    auth_service = provide(AuthService)
    user_service = provide(UserService)
    role_service = provide(RoleService)
    permission_service = provide(PermissionService)
