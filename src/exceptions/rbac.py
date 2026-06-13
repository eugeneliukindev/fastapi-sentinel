class InsufficientPermissionsError(Exception):
    pass


class RoleAlreadyAssignedError(Exception):
    def __init__(self) -> None:
        super().__init__("Role already assigned")
