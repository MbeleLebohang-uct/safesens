"""
Django settings for safesens project.
"""

import os
import ast

def get_list(text):
    return [item.strip() for item in text.split(",")]


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value

def get_value_from_env(name, default_value):
    if name in os.environ:
        return os.environ[name]
    return default_value

DEBUG = get_bool_from_env("DEBUG", True)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../public_html"))

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = get_list(
    os.environ.get("ALLOWED_HOSTS", "localhost, 127.0.0.1, upsitec.club, www.upsitec.club")
)

INSTALLED_APPS = [
    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third part apps
    'graphene_django',
    
    # Custom apps
    'safesens.pages', 
    'safesens.event',  
    'safesens.device', 
    'safesens.account',
    'safesens.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'safesens.urls'

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

WSGI_APPLICATION = 'safesens.wsgi.application'

# Django GraphQL JWT settings
GRAPHQL_JWT = {"JWT_PAYLOAD_HANDLER": "safesens.account.utils.create_jwt_payload"}
if not DEBUG:
    GRAPHQL_JWT["JWT_VERIFY_EXPIRATION"] = True


AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHENE = {
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
    'SCHEMA': 'safesens.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
        # "safesens.middleware.JWTMiddleware",

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_value_from_env("DBNAME", 'development'),
        'USER': get_value_from_env("DBUSER", 'db_admin'),
        'PASSWORD': get_value_from_env("DBPASSWORD", 'ElephantsFly'),
        'HOST': get_value_from_env("DBHOST", 'n3plcpnl0283.prod.ams3.secureserver.net'),
        'PORT': get_value_from_env("DBPORT", '3306'),
        'OPTIONS': {
            'init_command': 'SET innodb_strict_mode=1',
            'charset': 'utf8mb4',
        }
    }
}

ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL = get_bool_from_env(
    "ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL", False
)

AUTH_USER_MODEL = "account.User"

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
