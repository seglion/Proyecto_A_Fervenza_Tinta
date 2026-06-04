#!/bin/bash
set -e

export PYTHONPATH=/workspace/backend/src:/workspace/backend

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Uvicorn server..."
exec "$@"
