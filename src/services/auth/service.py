from src.core.uow import UnitOfWork
from src.dto import TokenPayloadDTO
from src.enums import TokenType
from src.exceptions.auth import InvalidCredentialsError
from src.schemas.auth import LoginRequestSchema, TokenResponseSchema
from src.services.auth.blacklist import TokenBlacklistService
from src.services.auth.crypto.jwt import create_access_token, create_refresh_token, decode_token
from src.services.auth.crypto.password import verify_password


class AuthService:
    def __init__(self, uow: UnitOfWork, blacklist_service: TokenBlacklistService) -> None:
        self._uow = uow
        self._blacklist_service = blacklist_service

    async def login(self, data: LoginRequestSchema) -> TokenResponseSchema:
        user = await self._uow.users.get_by_email(data.email)
        if user is None or not await verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError
        return TokenResponseSchema(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def access(self, token: str) -> TokenPayloadDTO:
        return await self._validate_token(token, TokenType.ACCESS)

    async def refresh(self, token: str) -> TokenResponseSchema:
        payload = await self._validate_token(token, TokenType.REFRESH)
        await self._blacklist_service.blacklist_token(payload)
        await self._uow.commit()
        return TokenResponseSchema(
            access_token=create_access_token(payload.sub),
            refresh_token=create_refresh_token(payload.sub),
        )

    async def logout(self, access_token: str, refresh_token: str) -> None:
        access_payload = await self._validate_token(access_token, TokenType.ACCESS)
        refresh_payload = await self._validate_token(refresh_token, TokenType.REFRESH)
        await self._blacklist_service.blacklist_token(access_payload)
        await self._blacklist_service.blacklist_token(refresh_payload)
        await self._uow.commit()

    async def _validate_token(self, token: str, expected_type: TokenType) -> TokenPayloadDTO:
        payload = decode_token(token, expected_type)
        if await self._blacklist_service.is_blacklisted(payload.jti):
            raise InvalidCredentialsError
        return payload
