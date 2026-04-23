#!/bin/bash
set -e

echo "Starting Superset initialization..."

# Run database migrations
echo "Running database upgrades..."
superset db upgrade

# Initialize Superset
echo "Initializing Superset..."
superset init

# Start Superset with Gunicorn
echo "Starting Superset server..."
exec gunicorn \
  --bind 0.0.0.0:8088 \
  --workers 4 \
  --worker-class gthread \
  --threads 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  "superset.app:create_app()"
