#!/bin/bash
set -e

echo "Running DB reset..."
poetry run python scripts/reset_db.py

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Running seeding script..."
poetry run python scripts/seed.py

# --- FIN ADVERTENCIA ---

echo "Starting Uvicorn server..."
# "exec $@" ejecuta el comando (CMD) principal del Dockerfile
exec "$@"