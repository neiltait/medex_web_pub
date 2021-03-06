"""
Django settings for medexCms project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

from monitor.loggers import monitor, InsightsLogStream

with open('./version.txt') as v_file:
    VERSION = v_file.read()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTH_TOKEN_NAME = 'medex_auth_token'
ID_TOKEN_NAME = 'medex_id_token'

REFRESH_TOKEN_NAME = 'medex_refresh_token'
DO_NOT_REFRESH_COOKIE = 'medex_do_not_refresh'

# All period times should be in seconds
REFRESH_PERIOD = int(os.environ.get('REFRESH_PERIOD', 10 * 60))  # refresh tokens every ** seconds (default 10 minutes)
LOGOUT_IF_IDLE_PERIOD = int(os.environ.get('LOGOUT_IF_IDLE_PERIOD', 60 * 60))  # logout user if idle (default 1 hr)

# Note - docker url is API_URL=http://api:8000
API_URL = os.environ.get('API_URL', 'http://localhost:9000')
CMS_URL = os.environ.get('CMS_URL', 'http://localhost:12000')

OP_DOMAIN = os.environ.get('OP_DOMAIN')
OP_ISSUER = os.environ.get('OP_ISSUER', '/oauth/default')
OP_ID = os.environ.get('OP_ID')
OP_SECRET = os.environ.get('OP_SECRET')

APP_INSIGHTS_KEY = os.environ.get('APP_INSIGHTS_KEY', '')
if APP_INSIGHTS_KEY:
    monitor.change_log_stream(InsightsLogStream(APP_INSIGHTS_KEY))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
LOCAL = os.environ.get('LOCAL', False)

# Define the stage ('staging', etc), NB: LEAVE STAGE ENV VAR UNSET FOR PRODUCTION!
STAGE = os.environ.get('STAGE', None)

# REQUIRE_HTTPS should be set to False when running locally
REQUIRE_HTTPS = os.environ.get('REQUIRE_HTTPS', 'True').lower() == 'true'

ALLOWED_HOSTS = [
    'localhost',
    'medex-cms',
    'medical-examiner-staging-frontend-as.azurewebsites.net',
    'medical-examiners-cms-sandbox.azurewebsites.net',
    'medical-examiners-cms-staging.azurewebsites.net',
    'medex-web-pre.frontend.pre.medex.cloud',
    'medex-web-prd.frontend.prd.medex.cloud',
    'medex-uat.methods.co.uk',
    'medex.methods.co.uk',
    'medex-web-pre-ukw.frontend.pre.medex.cloud',
    'testserver',
    'medex-web-pre-2.azurewebsites.net',
]

EMAIL_WHITELIST = [
    '@nhs.uk',
    '@nhs.net',
    '.nhs.uk',
    '.nhs.net',
    '@methods.co.uk',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'alerts.apps.AlertsConfig',
    'errors.apps.ErrorsConfig',
    'examinations.apps.ExaminationsConfig',
    'home.apps.HomeConfig',
    'locations.apps.LocationsConfig',
    'people.apps.PeopleConfig',
    'permissions.apps.PermissionsConfig',
    'users.apps.UsersConfig',
    'sass_processor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'applicationinsights.django.ApplicationInsightsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'medexCms.urls'

WSGI_APPLICATION = 'medexCms.wsgi.application'

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, "medexCms/staticfiles/css/")

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

SASS_OUTPUT_STYLE = 'compact'

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, "medexCms/staticfiles/scss/"),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "medexCms/templates/"),
        ],
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

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "medexCms/staticfiles"),
]
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

if not DEBUG:
    APPLICATION_INSIGHTS = {
        # (required) Your Application Insights instrumentation key
        'ikey': APP_INSIGHTS_KEY,

        # (optional) By default, request names are logged as the request method
        # and relative path of the URL.  To log the fully-qualified view names
        # instead, set this to True.  Defaults to False.
        'use_view_name': True,

        # (optional) To log arguments passed into the views as custom properties,
        # set this to True.  Defaults to False.
        'record_view_arguments': False,

        # (optional) Exceptions are logged by default, to disable, set this to False.
        'log_exceptions': True,

        # (optional) Events are submitted to Application Insights asynchronously.
        # send_interval specifies how often the queue is checked for items to submit.
        # send_time specifies how long the sender waits for new input before recycling
        # the background thread.
        'send_interval': 1.0,  # Check every second
        'send_time': 3.0,  # Wait up to 3 seconds for an event

        # (optional, uncommon) If you must send to an endpoint other than the
        # default endpoint, specify it here:
        # 'endpoint': "https://dc.services.visualstudio.com/v2/track",
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': './debug.log',
            },
            'appinsights': {
                'class': 'applicationinsights.django.LoggingHandler',
                'level': 'DEBUG'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout
            }
        },
        'loggers': {
            'django': {
                'handlers': ['appinsights', 'file', 'console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
