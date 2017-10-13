from eatsmart.settings.dev import *   # noqa

import dj_database_url

DATABASES['default'].update(dj_database_url.config())
