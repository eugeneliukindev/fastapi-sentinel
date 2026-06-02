from dishka import Provider, Scope, provide

from src.core.uow import UnitOfWork
from src.services.auth.blacklist import TokenBlacklistService
from src.services.auth.service import AuthService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_token_blacklist_service(self, uow: UnitOfWork) -> TokenBlacklistService:
        return TokenBlacklistService(uow)

    @provide
    def get_auth_service(self, uow: UnitOfWork, blacklist_service: TokenBlacklistService) -> AuthService:
        return AuthService(uow, blacklist_service)
