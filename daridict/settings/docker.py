from os import environ

from django.core.exceptions import ImproperlyConfigured

from .base import *


debug_value = environ.get('DEBUG', 'false').strip().lower()
if debug_value not in {'1', 'true', '0', 'false'}:
    raise ImproperlyConfigured('DEBUG must be true, false, 1, or 0.')
DEBUG = debug_value in {'1', 'true'}

SECRET_KEY = environ.get('SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured('SECRET_KEY must be set when DEBUG is disabled.')
    from .dev import SECRET_KEY

ALLOWED_HOSTS = [
    host.strip()
    for host in environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,[::1]').split(',')
    if host.strip()
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': environ.get('POSTGRES_HOST', 'postgres'),
        'PORT': environ.get('POSTGRES_PORT', '5432'),
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
