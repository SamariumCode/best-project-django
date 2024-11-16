from decouple import config
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'rosetta',
    'dbbackup',
    'django_extensions',
    'rest_framework',
    'django_celery_beat',

    'core.apps.CoreConfig',
    'store.apps.StoreConfig',
    'ticket.apps.TicketConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # This comes after the custom middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



INTERNAL_IPS = ['127.0.0.1', '172.18.0.1', '0.0.0.0']

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', 'ticket/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'ticket.context_processors.get_pending_tickets',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': config('POSTGRES_ENGINE'),
        'NAME': config('POSTGRES_NAME'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', cast=int),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = config('LANGUAGE_CODE', default='fa')
TIME_ZONE = config('TIME_ZONE', default='Asia/Tehran')

languages_env = config('LANGUAGES', default='fa:Persian,en:English')
LANGUAGES = [(lang.split(':')[0], _(lang.split(':')[1])) for lang in languages_env.split(',')]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'core', 'locale')]

TIME_ZONE = config('TIME_ZONE', default='UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static and media files
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'core.CustomUser'

# Redis settings for caching and Celery
REDIS_URL = config('REDIS_URL')
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')

# Cache settings using Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', 'redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# For session engine
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Celery Configuration Options
CELERY_BROKER_URL = config('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = config('TIME_ZONE', 'UTC')



DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'INTERCEPT_REDIRECTS': False,
}


DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/usr/src/app/backups'}



DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"


AWS_ACCESS_KEY_ID = '6205efee-88d1-4d21-8499-cae334c8198d'

AWS_SECRET_ACCESS_KEY = 'b2dfacbb244e11e66f719225b30c5e08d38430602046aca59d348eea38440c24'

AWS_S3_ENDPOINT_URL = 'https://djangorestframework-shoponline.s3.ir-thr-at1.arvanstorage.ir'

AWS_STORAGE_BUCKET_NAME = 'djangorestframework-shoponline'

AWS_SERVICE_NAME = 's3'

AWS_S3_FILE_OVERWRITE = False
