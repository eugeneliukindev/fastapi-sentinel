class InsufficientPermissionsError(Exception):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message)


class RoleAlreadyAssignedError(Exception):
    def __init__(self, message: str = "Role already assigned") -> None:
        super().__init__(message)
