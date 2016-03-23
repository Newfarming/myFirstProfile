"""
Django settings for Brick project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PINBOT_DIR = os.path.dirname(BASE_DIR)

from django.conf import global_settings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')(addnx&mnf)72dr-tb6*=-^=i_cqseq75@vg4zueysmz((h!q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'qz.pinbot.me',
    'test.pinbot.me',
    u'qz.pinbot.me',
    u'test.pinbot.me',
]

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'xadmin',
    'debug_toolbar',
    'crispy_forms',
    'south',
    'compressor',
    'notifications',
    'ws4redis',
    'raven.contrib.django.raven_compat',
)

BRICK_PUB_APP = (
    'Brick',
    'Brick.App.system',
    'Brick.App.account',
    'Brick.App.job_hunting',
    'Brick.App.my_resume',
    'Brick.App.notify',
    'Brick.App.chat',
    'Brick.App.run',
)

PINBOT_PUB_APP = (
    'Pinbot',
    'app.pinbot_point',
    'app.payment',
    'app.sendemail',
    'feed',
    'jobs',
    'crm',
    'points',
    'taocv',
    'transaction',
    'pinbot_package',
    'users',
    'resumes',
    'app.invite',
    'app.dash',
    'app.vip',
    'app.partner',
)

INSTALLED_APPS += BRICK_PUB_APP
INSTALLED_APPS += PINBOT_PUB_APP

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
)

ROOT_URLCONF = 'Brick.urls'

WSGI_APPLICATION = 'Brick.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pinbot',
        'USER': 'yuege',
        'PASSWORD': '2115_pb_hp',
        'HOST': '10.160.24.216',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TIME_ZONE = 'Asia/Shanghai'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_PATH = os.path.join(BASE_DIR, 'static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')

STATICFILES_DIRS = (
    STATIC_PATH,
    os.path.join(PINBOT_DIR, 'public/')
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # copressor
    'compressor.finders.CompressorFinder',
)

# media path
MEDIA_PATH = os.path.join(BASE_DIR, 'media/')
MEDIA_ROOT = MEDIA_PATH + 'root/'
MEDIA_URL = '/media/'

# template dir
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'ws4redis.context_processors.default',
)

# rabbitmq conf
RABBITMQ_CONF = {
    'host': '127.0.0.1',
    'user': 'admin',
    'password': 'Rabbitmq2014',
    'port': '5672',
}

BROKER_URL = 'amqp://{user}:{password}@{host}:{port}'.format(**RABBITMQ_CONF)

# django admin bootstrap conf
BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

# redis cache setting
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:Redis2014@127.0.0.1:6379/0",
        "OPTIONS": {
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

# session backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_REDIS_PREFIX = 'session'

# sync resume api
PINBOT_PID = 'e40d8f62'
PINBOT_AES_KEY = '71818f2933314fa7926c05a38e354ca7'
SYNC_RESUME_API = 'http://127.0.0.1:8080/brick_api/v1/sync_resume/'
SEND_RESUME_API = 'http://127.0.0.1:8080/brick_api/v1/send_resume/'

# websocket
WEBSOCKET_URL = '/ws/'
WS4REDIS_CONNECTION = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 3,
    'password': 'Redis2014',
}
WS4REDIS_EXPIRE = 5
WS4REDIS_PREFIX = 'ws'

# login
LOGIN_URL = '/account/login/'

# mongo settings
MONGO_CONN = {
    'host': 'db1.pinbot.me:27017,db2.pinbot.me:27017,db3.pinbot.me:27017',
    'port': 27017,
    'user': 'yuange',
    'password': 'Hp_pb_2115',
}

MONGO_URI = 'mongodb://%(user)s:%(password)s@%(host)s/recruiting?replicaSet=rs0&readPreference=secondaryPreferred' % MONGO_CONN

# company card api
COMPANY_CARD_API = 'http://www.pinbot.me/companycard/job/interest?token={token}&interest={interest}'

# pinbot url
ACTIVE_URL = 'http://www.pinbot.me/users/valid_bduser/{token}'
RESUME_URL = 'http://www.pinbot.me/resumes/display/{resume_id}/0?job_id={job_id}'
SEND_RESUME_URL = 'http://www.pinbot.me/feed/receive_resume/'
RESUME_BOUGHT_URL = 'http://www.pinbot.me/transaction/bought/'
RECEIVE_URL = 'http://www.pinbot.me/feed/receive_resume/'

# support email
SUPPORT_EMAIL_LIST = [
    'support@hopperclouds.com',
    'c2b@hopperclouds.com',
]

# email client
MAIL_CLIENT = 'sendcloud'

# recommend broker url
RECO_BROKER_URL = 'mongodb://celery:hopper201313@db1.pinbot.me,db2.pinbot.me,db3.pinbot.me:27017/celery?replicaSet=rs0&readPreference=secondaryPreferred'

# reco max count
RECO_MAX_COUNT = 10

# Raven Sentry settings
RAVEN_CONFIG = {
    'dsn': 'http://f9bc74260ac344dd83a6cebce11058d4:aba0a58148e04198b002697f42b8c7d6@sentry.pinbot.me/2',
    'release': 'f3f775faadd811e4958db8e8561b8184',
}
CELERYD_HIJACK_ROOT_LOGGER = False
SENTRY_AUTO_LOG_STACKS = True

# logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handler': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'error': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/data/brick/log/django/django_error.log',
            'maxBytes': '1024 * 1025 * 5',
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'warn&error': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/data/brick/log/django/brick_exception.log',
            'maxBytes': '1024 * 1025 * 5',
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/data/brick/log/django/brick_info.log',
            'maxBytes': '1024 * 1025 * 5',
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['sentry', 'error'],
            'propagate': True,
            'level': 'INFO',
        },
        'brick.exception': {
            'handlers': ['sentry', 'warn&error'],
            'propagate': True,
            'level': 'WARNING',
        },
        'brick.info': {
            'handlers': ['info'],
            'level': 'INFO',
            'propagate': True,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
