from enum import StrEnum


class PermissionEnum(StrEnum):
    USERS_READ = "users:read"
    USERS_CREATE = "users:create"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"

    @property
    def description(self) -> str:
        resource, action = self.split(":")
        return f"{action.capitalize()} {resource}"
