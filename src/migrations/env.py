import asyncio

from importlib import import_module
from logging.config import fileConfig
from typing import no_type_check

from alembic import context
from geoalchemy2 import alembic_helpers
from roga_and_kopyta.config import settings
from roga_and_kopyta.models import Base
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


config.set_main_option(
    name="sqlalchemy.url",
    value=settings.DB_URL.unicode_string().replace("%", "%%"),
)
import_module(name="roga_and_kopyta.models")
target_metadata = Base.metadata

# NOTE: KEEP IT TO PREVENT DELETING POSTGIS SPECIAL TABLES!
@no_type_check
def include_name(name, type_, parent_names):
    if type_ == "table":
        return name in target_metadata.tables
    return True

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
        include_object=alembic_helpers.include_object,
        process_revision_directives=alembic_helpers.writer,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_name=include_name,
        include_object=alembic_helpers.include_object,
        process_revision_directives=alembic_helpers.writer,
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
