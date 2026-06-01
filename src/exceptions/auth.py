class InvalidCredentialsError(Exception):
    """Login failed, or the token's subject no longer maps to an existing user."""


class UserAlreadyExistsError(Exception):
    """Registration with an already taken username."""
