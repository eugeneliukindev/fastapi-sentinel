from src.exceptions.base import AppError


class UserNotFoundError(AppError):
    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message)
