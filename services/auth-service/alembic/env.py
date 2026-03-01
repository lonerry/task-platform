import asyncio
import logging
import os
import sys

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool, text
from sqlalchemy.ext.asyncio import AsyncEngine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.config import settings
from infrastructure.postgres.database import metadata
from infrastructure.postgres.models import *  # noqa: F401,F403


CREATE_SCHEMA_QUERY = f"CREATE SCHEMA IF NOT EXISTS {settings.POSTGRES_SCHEMA};"

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger(__name__)

target_metadata = metadata

config.set_main_option("sqlalchemy.url", settings.postgres_url)


def filter_foreign_schemas(name, type_, parent_names):
    return type_ != "schema" or name == settings.POSTGRES_SCHEMA


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=settings.POSTGRES_SCHEMA,
        include_schemas=True,
        include_name=filter_foreign_schemas,
    )

    with context.begin_transaction():
        connection.execute(text(CREATE_SCHEMA_QUERY))
        context.run_migrations()


async def run_migrations_online(engine: AsyncEngine):
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        ),
    )
    asyncio.run(run_migrations_online(connectable))
