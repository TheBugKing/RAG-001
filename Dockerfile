# Build stage not required for a simple Python app; single stage is fine.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Entrypoint runs migrations only when RUN_MIGRATIONS is set (e.g. in production).
# Local docker run: do not set RUN_MIGRATIONS → app starts without running migrations.
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000
CMD ["/app/scripts/entrypoint.sh"]
