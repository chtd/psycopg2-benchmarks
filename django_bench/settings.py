import os
import getpass

DEBUG = False
INSTALLED_APPS = [
        'django.contrib.contenttypes', 
        'django.contrib.auth',
        'django_extensions',
        'app',
    ]

DB_USER = os.environ.get('DB_USER', getpass.getuser())

DATABASES = {                                                                  
    'default': {                                                               
        'ENGINE': 'django.db.backends.postgresql_psycopg2',                    
        'NAME': 'psycopg2_cffi_test_db',                                                 
        'USER': DB_USER,                                                      
        'PASSWORD': '',                                                        
        'HOST': '',                                                            
        'PORT': '',                                                            
        }, 
    }
