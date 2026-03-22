import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.core.database import Base


# make sure to import all your models here for 'autogenerate' support
from app.modules.users.models import User
from app.modules.portfolio.models import Portfolio
from app.modules.transactions.models import Transaction

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set DB URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using AsyncEngine."""

    # 1. make engine
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    # 2. async function to run migrations
    async def do_run_migrations():
        # !!! FIX: use async with to open connection !!!
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations_sync)
        
        await connectable.dispose()

    # 3. Synchronous part (runs inside run_sync)
    def do_run_migrations_sync(connection: Connection):
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True # Important for tracking type changes
        )

        with context.begin_transaction():
            context.run_migrations()

    # 4. Run
    asyncio.run(do_run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()