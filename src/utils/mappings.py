from src.enums import PermissionEnum, RoleEnum

ROLE_PERMISSIONS = {
    RoleEnum.USER: [
        PermissionEnum.USERS_READ,
    ],
    RoleEnum.ADMIN: [
        PermissionEnum.USERS_READ,
        PermissionEnum.USERS_CREATE,
        PermissionEnum.USERS_UPDATE,
        PermissionEnum.USERS_DELETE,
    ],
}
