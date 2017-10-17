#!/bin/sh
/venv/bin/python manage.py migrate
/venv/bin/gunicorn eatsmart.wsgi:application -b 0.0.0.0:8000 --log-level=debug
