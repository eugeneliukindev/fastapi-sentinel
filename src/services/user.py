from sqlalchemy.exc import IntegrityError

from src.core.uow import UnitOfWork
from src.dto.user import UserInsertDTO, UserUpdateDTO
from src.enums import RoleEnum
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.exceptions.rbac import InsufficientPermissionsError, RoleAlreadyAssignedError
from src.exceptions.user import UserNotFoundError
from src.schemas.user import (
    UserChangePasswordSchema,
    UserCreateSchema,
    UserPartialUpdateSchema,
    UserReadSchema,
    UserReadWithRolesAndPermissionsSchema,
    UserReadWithRolesSchema,
    UserUpdateSchema,
)
from src.services.auth.crypto.password import get_password_hash, verify_password


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_all_users(self) -> list[UserReadSchema]:
        users = await self._uow.users.get_all()
        return [UserReadSchema(id=u.id, email=u.email) for u in users]

    async def create_user(self, data: UserCreateSchema) -> UserReadSchema:
        if await self._uow.users.get_by_email(data.email) is not None:
            raise UserAlreadyExistsError

        role = await self._uow.roles.get_by_name(RoleEnum.USER)
        if role is None:
            raise InvalidCredentialsError

        hashed_password = await get_password_hash(data.password)
        user = await self._uow.users.add(UserInsertDTO(email=data.email, hashed_password=hashed_password))
        user.roles.append(role)
        await self._uow.commit()

        return UserReadSchema(id=user.id, email=user.email)

    async def get_user_by_id(self, user_id: int) -> UserReadSchema:
        user = await self._uow.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return UserReadSchema.model_validate(user)

    async def get_user_by_id_with_roles(self, user_id: int) -> UserReadWithRolesSchema:
        user = await self._uow.users.get_by_id_with_roles(user_id)
        if user is None:
            raise UserNotFoundError
        return UserReadWithRolesSchema.model_validate(user)

    async def get_user_by_id_with_roles_and_permissions(self, user_id: int) -> UserReadWithRolesAndPermissionsSchema:
        user = await self._uow.users.get_by_id_with_roles_and_permissions(user_id)
        if user is None:
            raise UserNotFoundError
        return UserReadWithRolesAndPermissionsSchema.model_validate(user)

    async def replace_user(self, user_id: int, data: UserUpdateSchema) -> UserReadSchema:
        updated_user = await self._uow.users.update(user_id, UserUpdateDTO(email=data.email))
        if updated_user is None:
            raise UserNotFoundError

        await self._uow.commit()
        return UserReadSchema.model_validate(updated_user)

    async def update_user(self, user_id: int, data: UserPartialUpdateSchema) -> UserReadSchema:
        updated_user = await self._uow.users.update(user_id, UserUpdateDTO(**data.model_dump(exclude_unset=True)))
        if updated_user is None:
            raise UserNotFoundError

        await self._uow.commit()
        return UserReadSchema.model_validate(updated_user)

    async def change_password(self, user_id: int, data: UserChangePasswordSchema) -> None:
        user = await self._uow.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError

        if not await verify_password(data.current_password, user.hashed_password):
            raise InvalidCredentialsError

        hashed_password = await get_password_hash(data.new_password)
        await self._uow.users.update(user_id, UserUpdateDTO(hashed_password=hashed_password))
        await self._uow.commit()

    async def reset_user_password(self, user_id: int, new_password: str) -> None:
        user = await self._uow.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError

        hashed_password = await get_password_hash(new_password)
        await self._uow.users.update(user_id, UserUpdateDTO(hashed_password=hashed_password))
        await self._uow.commit()

    async def delete_user(self, user_id: int) -> UserReadSchema:
        deleted_user = await self._uow.users.delete(user_id)
        if deleted_user is None:
            raise UserNotFoundError

        await self._uow.commit()
        return UserReadSchema.model_validate(deleted_user)

    async def assign_role(self, user_id: int, role_id: int) -> UserReadWithRolesSchema:
        user = await self._uow.users.get_by_id_with_roles(user_id)
        role = await self._uow.roles.get_by_id(role_id)
        if user is None or role is None:
            raise InsufficientPermissionsError

        try:
            user.roles.append(role)
            await self._uow.commit()
        except IntegrityError as e:
            raise RoleAlreadyAssignedError from e
        return UserReadWithRolesSchema.model_validate(user)

    async def revoke_role(self, user_id: int, role_id: int) -> UserReadWithRolesSchema:
        user = await self._uow.users.get_by_id_with_roles(user_id)
        role = await self._uow.roles.get_by_id(role_id)
        if user is None or role is None:
            raise InsufficientPermissionsError

        user.roles.remove(role)
        await self._uow.commit()
        return UserReadWithRolesSchema.model_validate(user)
