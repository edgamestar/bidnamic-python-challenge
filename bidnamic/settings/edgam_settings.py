__author__ = 'Edward'

import os
import sys

from bidnamic.base_settings import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "bidnamic_db.sqlite3",
    }
}
