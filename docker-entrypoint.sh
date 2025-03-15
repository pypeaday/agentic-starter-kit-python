#!/bin/bash
set -e

export VIRTUAL_ENV=/opt/venv

# Run database migrations if alembic is available
if command -v alembic &> /dev/null; then
    echo "Running database migrations..."
    alembic upgrade head || echo "no migrations"
fi

# Start the application
echo "Starting web server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
