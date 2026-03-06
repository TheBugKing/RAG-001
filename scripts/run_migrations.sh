#!/usr/bin/env bash
# Run Alembic migrations. Use in CI/CD or before starting the app in production.
# Requires: DATABASE_URL (or same URL as in alembic.ini).
set -e
cd "$(dirname "$0")/.."
alembic upgrade head
