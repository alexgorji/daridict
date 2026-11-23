from os import environ

from .dev import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'postgres',
        'PORT': '5432',
        'NAME': environ['POSTGRES_DB'],
        'USER': environ['POSTGRES_USER'],
        'PASSWORD': environ['POSTGRES_PASSWORD'],
    },
}

STATIC_URL = '/static/'
LOGGING = {'version': 1, 'disable_existing_loggers': False}
