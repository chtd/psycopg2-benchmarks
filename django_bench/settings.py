import os
import getpass


try:
    import psycopg2
except ImportError:
    from psycopg2cffi import compat
    compat.register()

DEBUG = False
INSTALLED_APPS = [
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django_extensions',
        'app',
    ]

try:
    from psycopg2cffi import compat
    compat.register()
except ImportError:
    pass

TIME_ZONE = ''
DB_USER = os.environ.get('DB_USER', getpass.getuser())
SECRET_KEY = 'not so secret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'psycopg2_cffi_test_db',
        'USER': DB_USER,
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        },
    }
