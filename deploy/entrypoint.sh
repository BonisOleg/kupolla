#!/bin/sh
set -e

echo "=== Waiting for database ==="
until python3 -c "
import psycopg2, os
psycopg2.connect(
    dbname=os.environ.get('POSTGRES_DB', 'kupolla'),
    user=os.environ.get('POSTGRES_USER', 'kupolla'),
    password=os.environ.get('POSTGRES_PASSWORD', ''),
    host=os.environ.get('POSTGRES_HOST', 'db'),
    port=os.environ.get('POSTGRES_PORT', '5432'),
)
" 2>/dev/null; do
  echo "DB not ready — retrying in 2s..."
  sleep 2
done
echo "=== DB ready ==="

echo "=== Running migrations ==="
python3 manage.py migrate --noinput

echo "=== Collecting static files ==="
python3 manage.py collectstatic --noinput

echo "=== Compiling translations ==="
python3 manage.py compilemessages --ignore=venv 2>/dev/null || true

echo "=== Starting gunicorn ==="
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
