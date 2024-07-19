#!/usr/bin/env sh
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py migrate
/opt/insumate/venv/bin/uwsgi --ini /opt/insumate/uwsgi.ini