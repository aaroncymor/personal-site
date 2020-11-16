"""
Django settings for personal_site project.

Generated by 'django-admin startproject' using Django 2.0.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import logging.config, logging

import yaml

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# Config
db_config = {}
config_env = os.getenv('CONFIG')
if config_env is not None:
    with open(config_env) as f:
        config_data = yaml.load(f)
    # load config    
    app_conf = config_data['personal_site']
    personal_site_conf = config_data['personal_site_api']

    DJANGO_SECRET_KEY = app_conf['secret_key']
    
    # load loggers
    logging.config.dictConfig(config_data['logging'])
    PERSONAL_SITE_LOGGER = logging.getLogger(personal_site_conf['logger'])

    # load database
    db_config = app_conf['db']
else:
    raise ImproperlyConfigured('CONFIG not set as an environment variable.')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'aaroncymor.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    # django-filebrowser requires to be before django.contrib.admin
    'grappelli',
    'filebrowser',

    # django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps 
    'tinymce',
    'rest_framework',
    'django_filters',
    'corsheaders',

    # internal
    'blog',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Django Cors
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'personal_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'personal_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {}
try:
    if db_config:
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': db_config['database'],
            'USER': db_config['user'],
            'PORT': db_config['port'],
            'PASSWORD': db_config['pass'],
            'HOST': db_config['host']
        }
except Exception:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media') # '/www/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static'); #'/www/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Accounts Settings
LOGIN_REDIRECT_URL = '/dashboard/'

# Tiny MCE Config
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "code,image,table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'width': '100%',
    'height': '350px', # fixed height
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

## TODO: Reference personal_site.core.utils.group_pagination
## Check if we need to make partitions for pagination.

# Grouping of pages. Basically how may page numbers you group by
# Example below woulb mean group by 3, which will appear like this.
# 1 2 3 >
# < 4 5 6 >
# < 7 8 9
#GROUPBY_PAGINATION = 2 # Can also be defined by config

CORS_ORIGIN_ALLOW_ALL = True

