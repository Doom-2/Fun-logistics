#!/bin/bash
python manage.py migrate --check
status=$?
if [ $status != 0 ]; then
  python manage.py migrate
fi

# Creates first admin in table 'User' if one does not exist.
# Credentials are taken from .env"
if [ "$DJANGO_SUPERUSER_NAME" ]; then
  python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_NAME"
fi

exec "$@"
