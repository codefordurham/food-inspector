web: gunicorn eatsmart.wsgi --timeout 600 --workers 4
worker: celery -A eatsmart-celery worker --loglevel=INFO
