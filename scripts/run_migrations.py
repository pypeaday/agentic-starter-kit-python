#!/usr/bin/env python3
import os
import sys
from pathlib import Path


def run_migrations():
    """Run database migrations."""
    try:
        print("Running database migrations...")
        result = os.system("alembic upgrade head")
        if result != 0:
            print("Migration failed!", file=sys.stderr)
            sys.exit(1)
        print("Migrations completed successfully.")
    except Exception as e:
        print(f"Error running migrations: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Ensure we're in the project root
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)
    run_migrations()
