from .base import *
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
WSGI_APPLICATION = 'config.wsgi.local.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/' + 'db.sqlite3',
    }
}
