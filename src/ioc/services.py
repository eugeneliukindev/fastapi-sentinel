from dishka import Provider, Scope, provide

from src.core.uow import UnitOfWork
from src.services.auth.service import AuthService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_auth_service(self, uow: UnitOfWork) -> AuthService:
        return AuthService(uow)
