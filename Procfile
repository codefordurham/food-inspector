web: gunicorn eatsmart.wsgi --timeout 600 --workers 4 -linfo
worker: celery -A eatsmart worker -linfo
beat: celery  -A eatsmart beat -linfo
