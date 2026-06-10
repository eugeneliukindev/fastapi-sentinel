from src.core.uow import UnitOfWork
from src.dto import TokenPayload
from src.dto.user import UserInsert
from src.enums import TokenType
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.models.rbac.role import RoleEnum
from src.models.user import User
from src.schemas.auth import TokenResponse
from src.schemas.user import UserRead
from src.services.auth.blacklist import TokenBlacklistService
from src.services.auth.crypto.jwt import create_access_token, create_refresh_token, decode_token
from src.services.auth.crypto.password import get_password_hash, verify_password


class AuthService:
    def __init__(self, uow: UnitOfWork, blacklist_service: TokenBlacklistService) -> None:
        self._uow = uow
        self._blacklist_service = blacklist_service

    async def register(self, username: str, password: str) -> UserRead:
        if await self._uow.users.get_by_username(username) is not None:
            raise UserAlreadyExistsError
        default_role = await self._uow.roles.get_by_name(RoleEnum.USER)
        if default_role is None:
            raise InvalidCredentialsError
        user = await self._uow.users.add(
            UserInsert(username=username, hashed_password=get_password_hash(password), role_id=default_role.id)
        )
        await self._uow.commit()
        return UserRead.model_validate(user)

    async def login(self, username: str, password: str) -> TokenResponse:
        user: User | None = await self._uow.users.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def logout(self, token: str) -> None:
        await self._revoke_refresh_token(token)

    async def access(self, token: str) -> UserRead:
        payload = await self._validate_token(token, TokenType.ACCESS)
        user = await self._uow.users.get_by_id_with_role_and_permissions(payload.sub)
        if user is None:
            raise InvalidCredentialsError
        return UserRead.model_validate(user)

    async def refresh(self, token: str) -> TokenResponse:
        payload = await self._revoke_refresh_token(token)
        return TokenResponse(
            access_token=create_access_token(payload.sub),
            refresh_token=create_refresh_token(payload.sub),
        )

    async def _revoke_refresh_token(self, token: str) -> TokenPayload:
        payload = await self._validate_token(token, TokenType.REFRESH)
        await self._blacklist_service.blacklist_token(payload)
        await self._uow.commit()
        return payload

    async def _validate_token(self, token: str, expected_type: TokenType) -> TokenPayload:
        payload = decode_token(token, expected_type)
        if await self._blacklist_service.is_blacklisted(payload.jti):
            raise InvalidCredentialsError
        return payload
