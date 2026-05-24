import os

from decouple import config

from .base import *  # noqa: F403

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Use SQLite for local dev when USE_SQLITE=true or PostgreSQL is unavailable
if config('USE_SQLITE', default=False, cast=bool) or not os.environ.get('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
