#!/bin/sh
set -e
echo "Running migrations..."
/root/.local/bin/uv run alembic upgrade head
echo "Migrations done. Starting application..."
exec /root/.local/bin/uv run python src/main.py
