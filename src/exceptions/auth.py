class InvalidCredentialsError(Exception):
    """Login failed, or the token's subject no longer maps to an existing user."""


class UserAlreadyExistsError(Exception):
    def __init__(self) -> None:
        super().__init__("User already exists")
