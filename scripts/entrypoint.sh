#!/usr/bin/env bash
# Run migrations only when RUN_MIGRATIONS is set (e.g. in production).
# When someone runs the image locally, do not set RUN_MIGRATIONS → migrations are skipped.
set -e
cd /app
if [ -n "$RUN_MIGRATIONS" ] && [ "$RUN_MIGRATIONS" != "0" ] && [ "$RUN_MIGRATIONS" != "false" ]; then
  echo "Running migrations..."
  alembic upgrade head
  echo "Migrations done."
fi
exec uvicorn main:app --host 0.0.0.0 --port 8000
