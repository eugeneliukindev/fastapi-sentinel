class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message)


class UserAlreadyExistsError(Exception):
    def __init__(self, message: str = "User already exists") -> None:
        super().__init__(message)
