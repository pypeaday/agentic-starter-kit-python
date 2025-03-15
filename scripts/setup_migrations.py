#!/usr/bin/env python3
import os
import sys
from pathlib import Path


def create_migrations_env():
    """Create the alembic env.py configuration file."""
    env_py_content = """from logging.config import fileConfig
import os
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the app directory to the Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from app.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    \"\"\"Run migrations in 'offline' mode.\"\"\"
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    \"\"\"Run migrations in 'online' mode.\"\"\"
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

    migrations_dir = Path("migrations")
    env_py_path = migrations_dir / "env.py"

    if not migrations_dir.exists():
        print("Initializing alembic...")
        os.system("alembic init migrations")

    print("Configuring alembic env.py...")
    env_py_path.write_text(env_py_content)


def create_initial_migration():
    """Create the initial migration if none exists."""
    versions_dir = Path("migrations/versions")
    if not versions_dir.exists() or not list(versions_dir.glob("*.py")):
        print("Creating initial migration...")
        os.system("alembic revision --autogenerate -m 'Initial migration'")
        return True
    return False


def main():
    """Main function to set up migrations."""
    # Ensure we're in the project root
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    # Create data directory if it doesn't exist
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    try:
        # Set up migrations environment
        create_migrations_env()

        # Create initial migration if needed
        if create_initial_migration():
            print("Initial migration created successfully.")
        else:
            print("Migrations already exist, skipping initial migration creation.")

    except Exception as e:
        print(f"Error setting up migrations: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
