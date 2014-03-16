from .base import *

FLAG_EMAIL_ALERTS = ['info@example.com', ]
PROJECT_EMAIL_ALERTS = ['info@example.com', ]

DATABASES['default']['NAME'] = 'test_' + DATABASES['default']['NAME']

SECRET_KEY = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf'

COMPRESS_ENABLED = False

COMPRESS_PRECOMPILERS = ()

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
