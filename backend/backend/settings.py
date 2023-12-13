import os
import environ
# from os import getenv, environ
from pathlib import Path
from decouple import config

import sentry_sdk
from django.template.context_processors import static
from django.templatetags.static import static
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://bf2dcbe2aa904d0eb04130471089544c@o1296528.ingest.sentry.io/6523315",
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = environ.Path(__file__) - 3

env = environ.Env()

env.read_env(ROOT_DIR(".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'import_export',
    'rest_framework',
    "debug_toolbar",

    'core_base',
    'industrial',

    'bulletin_board',
    'payment',
    'drf',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT', cast=int),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'LOCATION': 'http://127.0.0.1:8000',
        'LOCATION': 'unique-snowflake',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# DATE_INPUT_FORMATS = ['%d-%m-%Y']
# DATE_INPUT_FORMATS = ['%Y-%m-%d']

DATE_FORMAT = (('d-m-Y'))
DATE_INPUT_FORMATS = (('%d-%m-%Y'),)
DATETIME_FORMAT = (('d-m-Y H:i'))
DATETIME_INPUT_FORMATS = (('%d-%m-%Y %H:%i'),)

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_ROOT = os.path.join(ROOT_DIR, 'media_root/')
STATIC_ROOT = os.path.join(ROOT_DIR, 'static_root/')

# MEDIA_ROOT = env('MEDIA_ROOT')
# STATIC_ROOT = env('STATIC_ROOT')


STATIC_URL = 'static_root/'
MEDIA_URL = 'media_root/'

# STATICFILES_DIRS = [
#     ROOT_DIR + '/home/gregory/PycharmProjects/jobox/static',
# ]
#
# print(BASE_DIR)
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core_base.User'

JOB_PAYMENT_PRICES = {
    'ruble': 399,
    'bonus_point': 1
}

DOMAIN_NAME = env('DOMAIN_NAME')

TINKOFF_TERMINAL_KEY = env('TINKOFF_TERMINAL_KEY')
TINKOFF_TERMINAL_PASSWORD = env('TINKOFF_TERMINAL_PASSWORD')
TINKOFF_SUCCESS_URL = 'https://%s/industrial/payment_invoices/{invoice_id}/check' % DOMAIN_NAME

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
