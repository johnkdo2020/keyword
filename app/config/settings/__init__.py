import os

SETTING_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if not SETTING_MODULE or SETTING_MODULE == 'config.settings':
    from .local import *