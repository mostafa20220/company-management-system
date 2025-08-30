#!/bin/sh
python manage.py migrate  --noinput
echo "database migrated"
python manage.py collectstatic --noinput
echo "static files collected"

# Check if arguments are passed
if [ -z "$1" ]; then
  echo "No command provided. Running default command..."
  gunicorn companyManagementSystem.wsgi -b 0.0.0.0:8000 --disable-redirect-access-to-syslog --timeout 200  --workers=1 --threads=2 --worker-class=gthread --reload
else
  # Execute the passed command
  exec "$@"
fi

