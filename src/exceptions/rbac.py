class InsufficientPermissionsError(Exception):
    pass


class InvalidPermissionFormatError(ValueError):
    def __init__(self) -> None:
        super().__init__("format must be resource:action (e.g. users:read)")
