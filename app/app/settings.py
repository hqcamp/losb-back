import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))

SECRET_KEY = env.str('SECRET_KEY')
TECHSUPPORT_BOT_URL = env.str('TECHSUPPORT_BOT_URL')
TECHSUPPORT_BOT_TOKEN = env.str('TECHSUPPORT_BOT_TOKEN')
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

SMS_VERIFICATOIN_CODE_DIGITS = env.int('SMS_VERIFICATOIN_CODE_DIGITS')
SMS_VERIFICATION_RESEND_COOLDOWN = env.int('SMS_VERIFICATION_RESEND_COOLDOWN')
SMS_VERIFICATION_ATTEMPTS = env.int('SMS_VERIFICATION_ATTEMPTS')
SMS_RU_API_KEY = env.str('SMS_RU_API_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['*']
DOMAIN_NAME = env.str('DOMAIN_NAME', '')

# Application definition
PROJECT_APPS = [
    'losb'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'drf_standardized_errors',
    'django_extensions',
    'debug_toolbar',
    'corsheaders',
    *PROJECT_APPS
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_NAME'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.int('POSTGRES_PORT'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_standardized_errors.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'losb.api.v1.services.auth.CustomAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 15,
}
DRF_STANDARDIZED_ERRORS = {'ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS': True}
INTERNAL_IPS = ['127.0.0.1',]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

SPECTACULAR_SETTINGS = {
    'TITLE': 'losb API',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'ENUM_NAME_OVERRIDES': {
        'ValidationErrorEnum': 'drf_standardized_errors.openapi_serializers.ValidationErrorEnum.values',
        'ClientErrorEnum': 'drf_standardized_errors.openapi_serializers.ClientErrorEnum.values',
        'ServerErrorEnum': 'drf_standardized_errors.openapi_serializers.ServerErrorEnum.values',
        'ErrorCode401Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode401Enum.values',
        'ErrorCode403Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode403Enum.values',
        'ErrorCode404Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode404Enum.values',
        'ErrorCode405Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode405Enum.values',
        'ErrorCode406Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode406Enum.values',
        'ErrorCode415Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode415Enum.values',
        'ErrorCode429Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode429Enum.values',
        'ErrorCode500Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode500Enum.values',
    },
    'POSTPROCESSING_HOOKS': ['drf_standardized_errors.openapi_hooks.postprocess_schema_enums'],
}

AUTH_USER_MODEL = 'losb.User'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
