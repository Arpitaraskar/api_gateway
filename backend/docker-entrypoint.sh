#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

echo "Running database migrations..."
alembic upgrade head

echo "Starting User Service..."
exec python -m uvicorn services.user_service.main:app \
    --host 0.0.0.0 \
    --port 8001