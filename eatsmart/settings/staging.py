from eatsmart.settings.base import *

os.environ.setdefault('CACHE_HOST', '127.0.0.1:11211')
os.environ.setdefault('BROKER_HOST', '127.0.0.1:5672')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'eatsmart_staging'
DATABASES['default']['USER'] = 'eatsmart_staging'
DATABASES['default']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['default']['PASSWORD'] = os.environ['DB_PASSWORD']

PUBLIC_ROOT = '/var/www/eatsmart/public/'

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

EMAIL_SUBJECT_PREFIX = '[Eatsmart Staging] '

COMPRESS_ENABLED = True

# SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(';')

# Uncomment if using celery worker configuration
BROKER_URL = 'amqp://eatsmart_staging:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/eatsmart_staging' % os.environ

LOGGING['handlers']['file']['filename'] = '/var/www/eatsmart/log/inspections.log'
