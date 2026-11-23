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
WHITENOISE_USE_FINDERS = True
MIDDLEWARE = [
    MIDDLEWARE[0],
    'whitenoise.middleware.WhiteNoiseMiddleware',
    *MIDDLEWARE[1:],
]

LOGGING = {'version': 1, 'disable_existing_loggers': False}
