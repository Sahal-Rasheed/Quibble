import os
from pathlib import Path

import dj_database_url
import django_stubs_ext
from dotenv import load_dotenv

# monkeypatch django types
django_stubs_ext.monkeypatch()
# load envs
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'ilovequibble')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG', 1))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # auth related app on top
    'apps.user',
    # django middlewares
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django extensions
    'django_extensions',
    # rest framework
    'rest_framework',
    'rest_framework.authtoken',
    # custom error handling
    'drf_standardized_errors',
    # django filtering
    'django_filters',
    # middleware (cors)
    'corsheaders',
    # openapi
    'drf_spectacular',
    'drf_spectacular_sidecar',
    # apps
    'apps.quiblet',
    # file middleware (should be at last)
    'django_cleanup',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.user.auth.ExtendedTokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_standardized_errors.openapi.AutoSchema',
}

# https://drf-standardized-errors.readthedocs.io/en/latest/openapi.html#tips-and-tricks
DRF_STANDARDIZED_ERRORS = {
    'ALLOWED_ERROR_STATUS_CODES': ['400', '403', '404', '429'],
}

# https://drf-standardized-errors.readthedocs.io/en/latest/openapi.html#hide-error-responses-that-show-in-every-operation
with open(BASE_DIR / 'docs' / 'openapi_description.md') as f:
    openapi_description = f.read()

SPECTACULAR_SETTINGS = {
    'TITLE': 'QuibbleAPI',
    'DESCRIPTION': openapi_description,
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # sidecar config
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'defaultModelsExpandDepth': -1,
        'displayRequestDuration': True,
        'displayOperationId': True,
    },
    # integrate with drf-standardized-errors
    # https://drf-standardized-errors.readthedocs.io/en/latest/openapi.html#
    'ENUM_NAME_OVERRIDES': {
        'ValidationErrorEnum': 'drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices',
        'ClientErrorEnum': 'drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices',
        'ServerErrorEnum': 'drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices',
        'ErrorCode401Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices',
        'ErrorCode403Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices',
        'ErrorCode404Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices',
        'ErrorCode405Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices',
        'ErrorCode406Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices',
        'ErrorCode415Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices',
        'ErrorCode429Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices',
        'ErrorCode500Enum': 'drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices',
    },
    'POSTPROCESSING_HOOKS': [
        'drf_standardized_errors.openapi_hooks.postprocess_schema_enums',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # cors middleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    ),
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom AUTH model and backends
AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # custom auth backend
    'apps.user.backends.EmailAuthBackend',
]

# django-cors-headers settins
# https://pypi.org/project/django-cors-headers/

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
]

# max no:of profiles a user can create
PROFILE_LIMIT = 3

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Media files ( Images, Videos )
# https://docs.djangoproject.com/en/4.2/howto/static-files/#serving-uploaded-files-in-development

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
