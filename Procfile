web: gunicorn eatsmart.wsgi --timeout 600 --workers 4
worker: celery worker --beat -A eatsmart-celery --loglevel=INFO
