__author__ = 'Edward'

import os

from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# logs directory
LOGS_DIR = BASE_DIR / 'logs'

SECRET_KEY = '&=jdtcqr5ix_v1jubk)&$8a6s(r58^7*uhzq&3g0!n-hhs89yn'

# try to get system user's username
try:
    user = __file__.split('/')[2].lower()
except:
    user = __file__.split('\\')[2].lower()

# select settings file to use based on current user or use production settings
DEVS = ['edgam']
if user in DEVS:
    WHOSE = '{}_settings'.format(user)
    DEFAULT_URL_SCHEME = 'http'
else:
    WHOSE = 'prod_settings'
    DEFAULT_URL_SCHEME = 'https'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'portal.apps.PortalConfig',
    # 3rd party apps
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 3rd party middlewares
    'portal.middleware.UserRestrict',
]

ROOT_URLCONF = 'bidnamic.urls'

TEMPLATES_DIRS = [BASE_DIR / 'portal/templates']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 3rd party context processors
                'portal.context_processors.default',
            ],
        },
    },
]

WSGI_APPLICATION = 'bidnamic.wsgi.application'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MESSAGE_LEVEL = 10

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'portal.User'

AUTHENTICATION_BACKENDS = (
    'portal.authentication.CustomAuthBackend',
)

PASSWORD_RESET_TIMEOUT_DAYS = 1

CSRF_FAILURE_VIEW = 'portal.views.csrf_failure'

LOGIN_URL = reverse_lazy('auth', kwargs={'target': 'signin'})

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'd/m/Y H:i'

DATE_FORMAT = 'd/m/Y'

DATETIME_FORMATS = ['%y/%m/%d %H:%M:%S', '%Y/%m/%d %H:%M:%S']

STATIC_URL = '/bidnamic/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "portal/static"),
]

MEDIA_URL = '/bidnamic/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ADMINS = [('Edward Segun', 'edward@edwardsegun.com')]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "Edward Segun <do-not-reply@edwardsegun.com>"

EMAIL_USE_SSL = True
EMAIL_HOST = 'server.edwardsegun.com'
EMAIL_HOST_USER = 'do-not-reply@edwardsegun.com'
EMAIL_HOST_PASSWORD = 'computergeek#1'
EMAIL_PORT = 465

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# region Celery-related settings
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://127.0.0.1:6379/3',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CELERY_BROKER_URL = 'redis://localhost:6379/3'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
CELERY_TASK_DEFAULT_QUEUE = 'bidnamic_default_queue'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'
# endregion

# region Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bidnamic',)
}
# endregion
