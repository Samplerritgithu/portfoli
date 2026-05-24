#!/usr/bin/env bash
set -e

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"

echo "==> Django settings: $DJANGO_SETTINGS_MODULE"
echo "==> ALLOWED_HOSTS: ${ALLOWED_HOSTS:-<auto>}"
echo "==> Running migrations..."
python manage.py migrate --noinput

if [ "${RUN_SEED:-false}" = "true" ]; then
  echo "==> Seeding portfolio data..."
  python manage.py seed_portfolio
fi

echo "==> Starting Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
