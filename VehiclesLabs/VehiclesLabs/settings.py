"""
Django settings for VehiclesLabs project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from src.utils.main import *
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ol@xdd%&91a1-l2rtdy%b8+11v11^c*+byul(b(fk3hj(y#1f7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'rest_framework',
    # 'rest_framework.authtoken',
    # 'swagger_ui',
    
    'corsheaders',

    'storages',

    'django_filters',
    'drf_yasg',

    'src.apis.accounts',
    'src.apis.fueltype',
    'src.apis.vehiclebrands',
    'src.apis.customer',
    'src.apis.workshop',
    'src.apis.vehicles',
    'src.apis.jobcards',
    'src.apis.rolepermission',
    'src.apis.services',
    'src.apis.parts',
    'src.apis.media',
    'src.apis.vendorinventory',
    'src.apis.vendorcustomer',
    'src.apis.workshopinventory',
    'src.apis.countersale',
    'src.apis.vendors',
    'src.apis.customerBookAppointment',
    'src.apis.notifications',
    'src.apis.serviceReminder',
    'src.apis.vendorsalecard',
    'src.apis.admininquiry',
    'src.apis.accounting_software',
    ]


CRONJOBS = [
    ('0 8 * * *', 'VehicelsLabs.cron.service_reminder')
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CRON_CLASSES = [
    "src.apis.accounts.api.cron.MyCronJob",
]


CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'api_key',
]

ROOT_URLCONF = 'VehiclesLabs.urls'

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
},]

WSGI_APPLICATION = 'VehiclesLabs.wsgi.application'
GEOS_LIBRARY_PATH = '/home/bob/local/lib/libgeos_c.so'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("NAME", default=""),
        'USER': os.getenv("DB_USER", default=""),
        'PASSWORD': os.getenv("PASSWORD", default=""),
        'HOST': os.getenv("HOST", default=""),
        'PORT': os.getenv("PORT", default="")
    }
}

AUTH_USER_MODEL = 'accounts.UserDetail'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
MEDIA_URL = '/images/'

import datetime

from VehiclesLabs.aws.utils import *

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID",default="")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY",default="")
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'VehiclesLabs.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'VehiclesLabs.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME",default="")
AWS_S3_REGION_NAME = 'ap-south-1' 
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
AWS_DEFAULT_ACL = None

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


# import logging
# from boto3.session import Session


# AWS_REGION_NAME = 'ap-south-1'
# AWS_LOG_GROUP = "vehicleslabs",
# AWS_LOG_STREAM = 'vehicleslabs-stream', 
# AWS_LOGGER_NAME = 'watchtower-logger' 


# # logger
# boto3_session = Session(
#   aws_access_key_id=AWS_ACCESS_KEY_ID,
#   aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#   region_name=AWS_REGION_NAME
# )

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'aws': {
#             # you can add specific format for aws here
#             # if you want to change format, you can read:
#             #    https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python/44401529
#             'format': u"%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
#             'datefmt': "%Y-%m-%d %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'watchtower': {
#             'level': 'DEBUG',
#             'class': 'watchtower.CloudWatchLogHandler',
#             'boto3_session': boto3_session,
#             'log_group': 'vehicleslabs',
#             'stream_name': 'vehicleslabs-stream',
#             'formatter': 'aws', # use custom format
#         },
#     },
#     'loggers': {
#         AWS_LOGGER_NAME: {
#             'level': 'DEBUG',
#             'handlers': ['watchtower'],
#             'propagate': False,
#         },
#         # add your other loggers here...
#     },
# }


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        }
    },
}