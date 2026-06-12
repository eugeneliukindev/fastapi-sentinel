from sqlalchemy import delete

from src.core.uow import UnitOfWork
from src.dto.user import UserInsertDTO, UserUpdateDTO
from src.enums import RoleEnum
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.exceptions.rbac import InsufficientPermissionsError
from src.exceptions.user import UserNotFoundError
from src.models.association.user_roles import UserRolesOrm
from src.schemas.user import UserCreateS, UserReadS, UserReadWithRolesAndPermissionsS, UserReadWithRolesS, UserUpdateS
from src.services.auth.crypto.password import get_password_hash


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_all_users(self) -> list[UserReadS]:
        users = await self._uow.users.get_all()
        return [UserReadS(id=u.id, email=u.email) for u in users]

    async def create_user(self, data: UserCreateS) -> UserReadS:
        if await self._uow.users.get_by_email(data.email) is not None:
            raise UserAlreadyExistsError
        if (role := await self._uow.roles.get_by_name(RoleEnum.USER)) is None:
            raise InvalidCredentialsError
        hashed_password = await get_password_hash(data.password)
        user = await self._uow.users.add(UserInsertDTO(email=data.email, hashed_password=hashed_password))
        self._uow.session.add(UserRolesOrm(user_id=user.id, role_id=role.id))
        await self._uow.commit()
        return UserReadS(id=user.id, email=user.email)

    async def get_user_by_id(self, user_id: int) -> UserReadS:
        if (user := await self._uow.users.get_by_id(user_id)) is None:
            raise UserNotFoundError
        return UserReadS.model_validate(user)

    async def get_user_by_id_with_roles(self, id_: int) -> UserReadWithRolesS:
        if (user := await self._uow.users.get_by_id_with_roles(id_)) is None:
            raise UserNotFoundError
        return UserReadWithRolesS.model_validate(user)

    async def get_user_by_id_with_roles_and_permissions(self, id_: int) -> UserReadWithRolesAndPermissionsS:
        if (user := await self._uow.users.get_by_id_with_roles_and_permissions(id_)) is None:
            raise UserNotFoundError
        return UserReadWithRolesAndPermissionsS.model_validate(user)

    async def update_user(self, user_id: int, data: UserUpdateS) -> UserReadS:
        dto = UserUpdateDTO(**data.model_dump(exclude_unset=True))
        if (updated_user := await self._uow.users.update(user_id, dto)) is None:
            raise UserNotFoundError
        await self._uow.commit()
        return UserReadS.model_validate(updated_user)

    async def delete_user(self, user_id: int) -> UserReadS:
        if (deleted_user := await self._uow.users.delete(user_id)) is None:
            raise UserNotFoundError
        await self._uow.commit()
        return UserReadS.model_validate(deleted_user)

    async def assign_role(self, user_id: int, role_id: int) -> UserReadS:
        if (user := await self._uow.users.get_by_id(user_id)) is None or await self._uow.roles.get_by_id(
            role_id
        ) is None:
            raise InsufficientPermissionsError
        self._uow.session.add(UserRolesOrm(user_id=user_id, role_id=role_id))
        await self._uow.commit()
        return UserReadS.model_validate(user)

    async def revoke_role(self, user_id: int, role_id: int) -> None:
        if await self._uow.users.get_by_id(user_id) is None or await self._uow.roles.get_by_id(role_id) is None:
            raise InsufficientPermissionsError
        await self._uow.session.execute(
            delete(UserRolesOrm).where(
                UserRolesOrm.user_id == user_id,
                UserRolesOrm.role_id == role_id,
            )
        )
        await self._uow.commit()
