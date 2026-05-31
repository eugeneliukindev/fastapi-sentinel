from typing import ClassVar

from sqlalchemy import MetaData, inspect
from sqlalchemy.orm import DeclarativeBase

# Recommended SQLAlchemy naming convention so Alembic emits deterministic,
# human-readable names for indexes and constraints instead of backend defaults.
# https://docs.sqlalchemy.org/en/20/core/constraints.html#configuring-constraint-naming-conventions
_NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base for every ORM model.

    Import-pure on purpose: it depends only on SQLAlchemy, so ``Base.metadata`` can be
    imported by Alembic's ``env.py`` without pulling in application settings.
    """

    metadata = MetaData(naming_convention=_NAMING_CONVENTION)

    # Column attribute names to keep out of __repr__ (secrets: password hashes, tokens, ...).
    __repr_exclude__: ClassVar[frozenset[str]] = frozenset()

    def __repr__(self) -> str:
        """Show the persistence state and the currently loaded column values.

        Only loaded columns are read (expired/unloaded are skipped) and relationships are
        never touched, so repr never emits a query nor raises ``DetachedInstanceError``.
        """
        state = inspect(self)
        # SQLAlchemy object states (mutually exclusive):
        #   transient  - created in memory, never added to a session, no DB identity
        #   pending    - added to a session (session.add) but not yet flushed to the DB
        #   persistent - has a DB row and is attached to a session
        #   deleted    - marked for deletion within the current flush, not yet committed
        #   detached   - has a DB identity but is not attached to any session
        if state.transient:
            status = "transient"
        elif state.pending:
            status = "pending"
        elif state.deleted:
            status = "deleted"
        elif state.detached:
            status = "detached"
        else:
            status = "persistent"

        # state.unloaded = columns not currently in memory (expired/deferred/never set).
        # Skipping them means getattr only reads loaded values -> no extra query, no
        # DetachedInstanceError. column_attrs excludes relationships (no lazy load there either).
        fields = ", ".join(
            f"{attr.key}={getattr(self, attr.key)!r}"
            for attr in state.mapper.column_attrs
            if attr.key not in state.unloaded and attr.key not in self.__repr_exclude__
        )
        class_name = type(self).__name__
        return f"<{class_name} [{status}] ({fields})>"
