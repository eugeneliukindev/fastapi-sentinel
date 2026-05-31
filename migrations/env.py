import asyncio
import logging.config
import os

from alembic import context
from sqlalchemy import URL, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from models import Base

# There is no alembic.ini, so configure logging here instead of fileConfig(): this replaces
# the [loggers]/[handlers]/[formatters] sections and mirrors alembic's default console output.
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "generic": {"format": "%(levelname)-5.5s [%(name)s] %(message)s", "datefmt": "%H:%M:%S"},
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "generic", "stream": "ext://sys.stderr"},
        },
        "root": {"level": "WARNING", "handlers": ["console"]},
        "loggers": {
            "alembic": {"level": "INFO", "handlers": [], "propagate": True},
            "sqlalchemy.engine": {"level": "WARNING", "handlers": [], "propagate": True},
        },
    }
)

config = context.config

# Read the database connection straight from the environment, so migrations depend only on
# the DB env vars and never import the application settings. POSTGRES_* takes precedence
# (e.g. the postgres image vars), falling back to the app's MY_APP__DB__* names.
config.set_main_option(
    "sqlalchemy.url",
    URL.create(
        drivername=os.environ.get("MY_APP__DB__DRIVER", "postgresql+asyncpg"),
        username=os.environ.get("POSTGRES_USER") or os.environ["MY_APP__DB__USERNAME"],
        password=os.environ.get("POSTGRES_PASSWORD") or os.environ["MY_APP__DB__PASSWORD"],
        host=os.environ.get("POSTGRES_HOST") or os.environ.get("MY_APP__DB__HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT") or os.environ.get("MY_APP__DB__PORT", "5432")),
        database=os.environ.get("POSTGRES_DB") or os.environ["MY_APP__DB__NAME"],
    ).render_as_string(hide_password=False),
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
