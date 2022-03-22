__author__ = 'Edward'

import sys

from bidnamic.base_settings import *

DEBUG = False

ALLOWED_HOSTS = ['bidnamic.edwardsegun.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "bidnamic_db.sqlite3",
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] [%(levelname)s %(levelno)s] [%(filename)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'error.log',
            'formatter': 'standard',
        },
        'consumer': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'consumer.log',
            'formatter': 'standard',
            'maxBytes': 50000,
            'backupCount': 2,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
        'normal': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'default.log',
            'formatter': 'standard',
            'maxBytes': 50000,
            'backupCount': 2,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'normal': {
            'handlers': ['console', 'normal'],
            'level': 'DEBUG',
        },
        'consumer': {
            'handlers': ['consumer'],
            'level': 'DEBUG',
        },
    },
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
