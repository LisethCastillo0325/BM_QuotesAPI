"""Testing settings.

With these settings, tests run faster.
"""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY", default="7lEaACt4wsCjhdsjdhksdhjksdhkshdksjhdcbfd45454d")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}