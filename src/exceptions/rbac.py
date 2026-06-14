from src.exceptions.base import AppError


class InsufficientPermissionsError(AppError):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message)


class RoleAlreadyAssignedError(AppError):
    def __init__(self, message: str = "Role already assigned") -> None:
        super().__init__(message)
