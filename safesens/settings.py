"""
Django settings for safesens project.
"""

import os
import ast
import warnings

from django.utils.timezone import timedelta
from django.core.exceptions import ImproperlyConfigured

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

SITE_ID = 1

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../public_html"))

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = get_list(
    os.environ.get("ALLOWED_HOSTS", "localhost, 127.0.0.1, upsitec.club, www.upsitec.club")
)

_DEFAULT_CLIENT_HOSTS = "localhost,127.0.0.1"

ALLOWED_CLIENT_HOSTS = os.environ.get("ALLOWED_CLIENT_HOSTS", "upsitec.club, www.upsitec.club")
if not ALLOWED_CLIENT_HOSTS:
    if DEBUG:
        ALLOWED_CLIENT_HOSTS = _DEFAULT_CLIENT_HOSTS
    else:
        raise ImproperlyConfigured(
            "ALLOWED_CLIENT_HOSTS environment variable must be set when DEBUG=False."
        )

ALLOWED_CLIENT_HOSTS = get_list(ALLOWED_CLIENT_HOSTS)

ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL = get_bool_from_env(
    "ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL", False
)

EMAIL_HOST_USER = get_value_from_env("EMAIL_HOST_USER", '')
EMAIL_HOST_PASSWORD = get_value_from_env("EMAIL_HOST_PASSWORD", '')
EMAIL_HOST = "smtp.office365.com"
EMAIL_PORT = 587
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

ENABLE_SSL = get_bool_from_env("ENABLE_SSL", False)

if ENABLE_SSL:
    SECURE_SSL_REDIRECT = not DEBUG

INSTALLED_APPS = [
    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    "django.contrib.sites",
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third part apps
    'graphene_django',
    'versatileimagefield',
    
    # Custom apps
    'safesens.core', 
    'safesens.pages', 
    'safesens.event',  
    'safesens.device', 
    'safesens.account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'safesens.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, "templates")],
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

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "products": [
        ("product_gallery", "thumbnail__540x540"),
        ("product_gallery_2x", "thumbnail__1080x1080"),
        ("product_small", "thumbnail__60x60"),
        ("product_small_2x", "thumbnail__120x120"),
        ("product_list", "thumbnail__255x255"),
        ("product_list_2x", "thumbnail__510x510"),
    ],
    "background_images": [("header_image", "thumbnail__1080x440")],
    "user_avatars": [("default", "thumbnail__445x445")],
}

VERSATILEIMAGEFIELD_SETTINGS = {
    # Images should be pre-generated on Production environment
    "create_images_on_demand": get_bool_from_env("CREATE_IMAGES_ON_DEMAND", DEBUG)
}

PLACEHOLDER_IMAGES = {
    60: "images/placeholder60x60.png",
    120: "images/placeholder120x120.png",
    255: "images/placeholder255x255.png",
    540: "images/placeholder540x540.png",
    1080: "images/placeholder1080x1080.png",
}

DEFAULT_PLACEHOLDER = "images/placeholder255x255.png"

GRAPHQL_JWT = {
    "JWT_PAYLOAD_HANDLER": "safesens.account.utils.create_jwt_payload",
}

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_value_from_env("DBNAME", 'development'),
        'USER': get_value_from_env("DBUSER", 'db_admin'),
        'PASSWORD': get_value_from_env("DBPASSWORD", 'ElephantsFly'),
        'HOST': get_value_from_env("DBHOST", 'n3plcpnl0283.prod.ams3.secureserver.net'),
        'PORT': get_value_from_env("DBPORT", '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

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
