import os
import sys
import dj_database_url

from config.settings.base import *


SECRET_KEY = '9OQeQf90W1HY9KRlRpkBuP1Lbl0xgLsnwZuvmmRJg0HmjhlnL7E8OXmh6SiuQQKa'

DEBUG = False

DEVELOPMENT_MODE = False

ALLOWED_HOSTS = [
    '147.182.185.220',
    '127.0.0.1',
    'localhost',
    'foxstraat.com'
]
 
if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR /'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media-root'