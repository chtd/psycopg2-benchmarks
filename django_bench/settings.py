DEBUG = False
INSTALLED_APPS = ['app']

import getpass

DB_USER = getpass.getuser()

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
