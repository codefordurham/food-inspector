from eatsmart.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'eatsmart_production'
DATABASES['default']['USER'] = 'eatsmart_production'

EMAIL_SUBJECT_PREFIX = '[Eatsmart Prod] '

# Uncomment if using celery worker configuration
BROKER_URL = 'amqp://eatsmart_production:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/eatsmart_production' % os.environ
