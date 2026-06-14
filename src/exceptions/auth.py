from src.exceptions.base import AppError


class InvalidCredentialsError(AppError):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message)


class UserAlreadyExistsError(AppError):
    def __init__(self, message: str = "User already exists") -> None:
        super().__init__(message)
