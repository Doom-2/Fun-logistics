#!/bin/bash
python manage.py migrate --check
status=$?
if [ $status != 0 ]; then
  python manage.py migrate
fi

# Create first admin in table 'User' if one does not exist.
# Credentials are taken from .env"
if [ "$DJANGO_SUPERUSER_NAME" ]; then
  python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_NAME"
fi

# Perform initial data load from spreadsheet
python3 manage.py get_orders "$SPREADSHEET_NAME"

exec "$@"
