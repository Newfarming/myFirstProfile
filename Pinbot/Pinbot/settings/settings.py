# coding: utf-8

import os
from pymongo import ReadPreference

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
PROJECT_ROOT = '/'.join(PROJECT_ROOT.split('/')[:-1])
# Django settings for RecruitingWeb project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = PROJECT_ROOT + '/media'
MEDIA_ROOT_STAFF = PROJECT_ROOT + '/media/staff'
STATIC_PATH = os.path.join(PROJECT_ROOT, 'public/').replace('\\', '/')
BRICK_STATIC_PATH = os.path.join(
    PROJECT_ROOT, 'Brick/static/').replace('\\', '/')
PINBOT_STATIC_ROOT = os.path.join(
    PROJECT_ROOT, 'static_root/').replace('\\', '/')

PARSE_PATH = MEDIA_ROOT

ADMINS = (
    ('liyao', 'liyao@hopperclouds.com'),
    ('likaiguo', 'likaiguo@hopperclouds.com'),
    ('likaiguo', 'likaiguo.happy@163.com'),
    ('fangyuan', 'peaker@hopperclouds.com'),
    ('chenchao', 'chenchao@hopperclouds.com'),
    ('czc', 'chengzhichun@hopperclouds.com'),
)
RESUME_BUY_ADMINS = ('liuyunhe@hopperclouds.com', 'panyalan@hopperclouds.com', 'liuyue@hopperclouds.com',
                     'fangyuan@hopperclouds.com', 'liguangyi@hopperclouds.com', 'zhoubin@hopperclouds.com',
                     'wangchencheng@hopperclouds.com', 'liuyanbin@hopperclouds.com',
                     'dengwanying@hopperclouds.com', 'luowenlan@hopperclouds.com', 'zengchongyun@hopperclouds.com')

ACCOUNT_ACTIVATION_DAYS = 365
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'team@pinbot.me'
EMAIL_HOST_PASSWORD = 'hopper2013'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = '聘宝<team@pinbot.me>'

WEBSITE_HOST = 'www.pinbot.me'
WEBSITE = 'http://www.pinbot.me'

SERVICE_QQ = '2711824953'

COMPANY_CARD_EXPIRE_DAY = 7

PINBOT_ADMIN = set()
PINBOT_ADMIN.add(
    '2XG$I$R06}|2NRka+>-UN}!AAIO+*]Mpc-M{,S=S2>1VUdd8)D HT)i+-kuap7;y')
PINBOT_ADMIN.add('2XGIR062NRka')

SERVER_EMAIL = 'team@pinbot.me'
AUTH_PROFILE_MODULE = "users.UserProfile"

MEDIA_ROOT = '/data/pinbot/media'
MEDIA_ROOT_STAFF = '/data/pinbot/media/staff'

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pinbot',  # Or path to database file if using sqlite3.
        'USER': 'yuege',  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '10.168.20.129',
        'PASSWORD': '2115_pb_hp',  # Not used with sqlite3.
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        },
    },
}
OTHER_DATABASE = {
    'mongo': {
        'ENGINE': '',
        'name': 'recruiting',
        'user': 'yuange',
        'host': 'mongodb://yuange:Hp_pb_2115@db1.pinbot.me:27017,db2.pinbot.me:27017,db3.pinbot.me:27017/recruiting',
        'password': 'Hp_pb_2115',
        'port': '27017',
        'lexicon_collection': 'jobs_class_keywords',
        'replicaset': 'rs0',
        'tag_sets': [{'use': 'web'}],
    },
    'rabbitmq': {
        'ENGINE': '',
        'host': '127.0.0.1',
        'user': 'admin',
        'password': 'Rabbitmq2015',
        'html_resume_queue': 'htmlresume',
        'upload_resume_queue': 'uploadresume',
        'buy_resume_queue': 'buyresume',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'redis://:root@127.0.0.1:6379:1',
    },
}

spider_mongo_host = 'db1.pinbot.me,db2.pinbot.me,db3.pinbot.me'
SPIDERS_MONGO = {
    'name': 'spiders',
    'username': 'pinbot_spiders',
    'host': spider_mongo_host,
    'password': 'Hp_pb_2115_spider',
    'port': 27017,
    'read_preference': ReadPreference.SECONDARY_PREFERRED,
    'replicaset': 'rs0',
    'tag_sets': [{'use': 'data'}],
    'alias': 'spiders',
}

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'pinbot.me',
    'www.pinbot.me',
    u'pinbot.me',
    u'www.pinbot.me',
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 5
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PINBOT_STATIC_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # PROJECT_ROOT + "/public/",
    STATIC_PATH,
    BRICK_STATIC_PATH,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

COMPRESS_JS_FILTERS = (
    'compressor.filters.yuglify.YUglifyJSFilter',
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.yuglify.YUglifyCSSFilter',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q23tyr$tfgkpq1wqmhpv-7@c29&amp;kz&amp;-f&amp;)$va)a%@77#4$(5xb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'Pinbot.middleware.json_request.JSONMiddleware',
    'Pinbot.middleware.user_access.UserAccessMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Pinbot.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Pinbot.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + "/templates",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.core.context_processors.static',
    'django_mobile.context_processors.flavour',
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    'endless_pagination',
    'xadmin',
    'captcha',
    'crispy_forms',
    'django_nose',
    'south',
    'notifications',
    'django_mobile',
    'compressor',
    'corsheaders',
    'django_summernote',
    'django_nose',
    'corsheaders',
    'notifications',

    'jobs',
    'pinbot_permission',
    'pin_celery',

    'app.invite',
    'app.payment',
    'app.special_feed',
    'app.activity',
    'app.sendemail',
    'app.promotion_point',
    'app.telnet_api',
    'app.task_system',
    'app.resume',
)

PINBOT_PUB_APP = (
    'Pinbot',
    'app.pinbot_point',
    'app.payment',
    'feed',
    'jobs',
    'points',
    'taocv',
    'transaction',
    'pinbot_package',
    'users',
    'resumes',
    'app.dash',
    'app.vip',
    'app.tutorial',
    'app.partner',
    'app.crm',
    'app.weixin'
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

INSTALLED_APPS += PINBOT_PUB_APP
INSTALLED_APPS += BRICK_PUB_APP

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

resume_score_log = os.path.join(PROJECT_ROOT + '/logs/', 'common.log')

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_REDIS_PREFIX = 'session'

# Raven Sentry settings
RAVEN_CONFIG = {
    'dsn': 'http://f388349888604d458530d2259e65ac7e:37e85b872ba445dbaec42def4151c883@sentry.pinbot.me/3',
    'release': 'f388349888604d458530d2259e65ac7e',
}
CELERYD_HIJACK_ROOT_LOGGER = False
SENTRY_AUTO_LOG_STACKS = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'tokenapi.backends.TokenBackend',
    'users.runtime.auth_backend.AuthPhoneBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 或者直接写路径：'c://logs/all.log',
            'filename': os.path.join(PROJECT_ROOT + '/logs/', 'all.log'),
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'common_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 或者直接写路径：'c://logs/all.log',
            'filename': os.path.join(PROJECT_ROOT + '/logs/', 'common.log'),
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'resume_score_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 或者直接写路径：'c://logs/all.log',
            'filename': os.path.join(PROJECT_ROOT + '/logs/', 'resume_score.log'),
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'email_send': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT + '/logs/', 'email_send.log'),
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,
            'formatter': 'standard',
            'filters': ['require_debug_false'],
        },
        'user_access': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT + '/logs/', 'user_access.log'),
            'maxBytes': 1024 * 1024 * 300,  # 300 MB
            # 'when': 'midnight',
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['sentry', 'default'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['sentry', 'common_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'resume_score': {
            'handlers': ['resume_score_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'email_send': {
            'handlers': ['email_send'],
            'level': 'INFO',
            'propagate': True,
        },
        'user_access': {
            'handlers': ['user_access'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}


LOGIN_URL = "/signin/"

DOCUMENT_PARSE_PORT = 'http://127.0.0.1:8080/parser/document/parse'

MAIL_KEY = "dme3pr3bp9hlkialoj7qs63eo9qicjjni1dics8iabj7d49pse3p888aa57455c645k0fn8depndebr1dnjs3"

PINBOT_ADMIN_AUTH_DICT = {
    'x-pinbot-admin-auth': '2XG$I$R06}|2NRka+>-UN}!AAIO+*]Mpc-M{,S=S2>1VUdd8)D HT)i+-kuap7;y'}

from datetime import datetime
REGISTER_DEADLINE = datetime(
    year=2014, month=2, day=7, hour=18, minute=0, second=0)
USER_FEED_AMOUNT_LIMIT = 5
USER_FEED_NEW_LIMIT = 2

import jieba
jieba_user_dict_file = os.path.join(PROJECT_ROOT, 'resource/userdict.txt')
jieba.load_userdict(jieba_user_dict_file)

DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

EMAIL_USERS = (
    ('liyao', 'liyao@hopperclouds.com'),
    ('likaiguo', 'likaiguo@hopperclouds.com'),
    ('fangyuan', 'peaker@hopperclouds.com'),
    ('liuyue', 'liuyue@hopperclouds.com'),
    ('yunhe', 'liuyunhe@hopperclouds.com'),
    ('shiwei', 'shiwei@hopperclouds.com'),
)
SUPPORT_EMAIL_LIST = (
    'support@hopperclouds.com',
)
ALLOWED_USERS = [email for _, email in EMAIL_USERS]
ALIAPY_HOST = 'http://pinbot.me/payment/alipay_return/'
API_PARSE_URL = 'http://127.0.0.1:1324/api/parse/resume/'
API_PARSE_JD_URL = 'http://10.171.224.66:8088/job/parser/'
API_PARSE_NUM = 'http://10.171.224.66:8088/search/resume/num/'
API_PARSE_SALARY = 'http://10.171.224.66:8088/datamining/salary/suggest/'
API_PARSE_RELATED = 'http://10.171.224.66:8088/talent/related/'

API_SEARCH_JOB = 'http://10.171.224.66:8088/search/job/'
API_SEARCH_RESUME = 'http://10.171.224.66:8088/search/resume/'
API_WRITE_ES = 'http://10.171.224.66:8088/search/insert/'

PASSWORD_RESET_TIMEOUT_DAYS = 2
PARSE_PATH = MEDIA_ROOT + '/'
FILE_UPLOAD_TEMP_DIR = '/media/disk1/data/django_tmp'
BRICK_CARD_TOKEN = 'd42MhXudCBfbnbJ9NqWJSC'

MARK_TIME = datetime(2015, 5, 13)

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    'width': '100%',
    'height': '480',

    # Use proper language setting automatically (default)
    # Or, set editor language/locale forcely
    'lang': 'zh-CN',


    # Customize toolbar buttons
    'toolbar': [
        ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript', 'strikethrough', 'clear']],
        # ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video', 'hr']],
        ['view', ['fullscreen', 'codeview']],
        ['help', ['help']],
    ],

    # Need authentication while uploading attachments.
    'attachment_require_authentication': False,

    # Set `upload_to` function for attachments.
    # 'attachment_upload_to': my_custom_upload_to_func(),

    # Set custom storage class for attachments.
    # 'attachment_storage_class': 'my.custom.storage.class.name',

    # Set external media files for SummernoteInplaceWidget.
    # !!! Be sure to put {{ form.media }} in template before initiate summernote.
    'inplacewidget_external_css': (
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
        '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',
    ),
    'inplacewidget_external_js': (
        '//code.jquery.com/jquery-1.9.1.min.js',
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    ),
}

USER_ACCESS_MIDDLEWARE_CONFIG = {
    'disable': (
        'admin', 'app.dash', 'app.crm', 'app.sendemail'
    ),
    'enable': {
        'app.special_feed': [
            '/special_feed/',
        ],
        'feed': [
            '/feed/',
            '/feed/feedFrequency/',
            '/feed/receive_resume/'
        ],
        'resumes': [
            '/resumes/display/',
            '/resumes/watch/',
            '/resumes/add_watch/',
        ],
        'transaction': [
            '/transaction/bought/',
            '/transaction/unmark_resume/',
            '/transaction/mark_resume/'
        ],
        'app.partner': [
            '/partner/reco_task/',
            '/partner/task_manage/',
            '/partner/resume_manage/',
            '/partner/home/'

        ],
        'app.payment': [
            '/payment/my_account/',
            '/payment/my_package/',
            '/payment/trade_log/',
            '/payment/point_record/',
            '/payment/coin_record/',
            '/payment/coin_recharge/',
            '/payment/point_recharge/'
        ],
        'companycard': [
            '/companycard/get/'
        ],
        'users': [
            '/users/profile/'
        ],
        'app.promotion_point': [
            'promotion_point/link/'
        ],
        'app.vip': [
            '/vip/role_info/'
        ]

    },
    'custom': {
        'app.sendemail': {
            'view_send': ['SendEmail.GET', 'SendEmail.POST']
        }
    }
}

CORS_ORIGIN_WHITELIST = (
    'm.pinbot.me',
)
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_DOMAIN = '.pinbot.me'
WEIXIN_HOST = 'm.pinbot.me'
WEIXIN_APP_ID = 'wx1eb151c698eb62cf'
WEIXIN_APP_SECERT = 'd678b26505b91280517e7a3d943e0bff'
WEIXIN_TOKEN = '960a31dd8c162518e77a37941802ee18'
WEIXIN_MCHID = '1233664702'
WEIXIN_PAY_KEY = 'YarOzSpKWG4TluDSJI45QhIN5gDT7Rnx'
WEIXIN_ACCESS_TOKEN_EXPIRE_TIME = 300
WEIXIN_OAUTH_REDIRECT_URL = 'http://m.pinbot.me/weixin/authorization?next_url=%s'
QRCODE_BIND_TOKEN_EXPIRE_TIME = 60 * 20
WEIXIN_MENU = {
    "button": [
        {
            "name": "我的职位",
            "sub_button": [
                {
                    "type": "click",
                    "name": "查看职位",
                    "key": "KEY_VIEW_JOB"
                },
                {
                    "type": "view",
                    "name": "新增定制",
                    "url": "http://m.pinbot.me/#/customize/new/?from=weixin"
                }
            ]
        },
        {
            "type": "view",
            "name": "查看推荐",
            "url": "http://m.pinbot.me/#/recommand/list/?from=weixin"
        },
        {
            "name": "个人中心",
            "sub_button": [
                {
                    "type": "click",
                    "name": "注册绑定",
                    "key": "KEY_BIND_ACCOUNT"
                },
                {
                    "type": "click",
                    "name": "联系我们",
                    "key": "KEY_CONTACT_US"
                },
                {
                    "type": "click",
                    "name": "操作指南",
                    "key": "KEY_HELP"
                },
                {
                    "type": "view",
                    "name": "招聘二三事",
                    "url": "http://mp.weixin.qq.com/s?__biz=MzAxMzI2MTg5NA==&mid=209239672&idx=1&sn=ee025c94cce3e6b291e80ffb95072ad3#rd"
                }
            ]
        }
    ]
}
WEIXIN_TEMPLATE_MSG_ID = '79V5-kEfejJD5WzxUk8T1om27-D2IBeLSLEM4B-NqFc'

# sms settings
SMS_CODE_EXPIRE_TIME = 60 * 20
SMS_SEND_URL = 'http://yunpian.com/v1/sms/send.json'
SMS_SEND_APIKEY = 'f0a698b6bb84ba82650053197ba5ebfa'
SMS_TEMPLATES = {
    'AccountReg': '【聘宝招聘】欢迎注册，你的校验码是%s，校验码有效期为%s分钟，请尽快验证使用。',
    'ChangePwd': '【聘宝招聘】你正在修改密码，请输入校验码%s，校验码有效期为%s分钟，请尽快验证使用。',
    'ChangeMobile': '【聘宝招聘】你正在修改手机号，请输入校验码%s，校验码有效期为%s分钟，请尽快验证使用。'
}
SMS_SNED_MAX_COUNT = 5

# notify email settings
EMAIL_TOKEN_EXPIRE_TIME = 60 * 30

# token api expire time
TOKEN_TIMEOUT_DAYS = 60
TOKEN_CHECK_ACTIVE_USER = True

SPIDER_MSG_TOKEN_REQ_URL = 'http://10.171.224.66:5100/resumes/login/'
SPIDER_DOWNLOAD_MSG_REQ_URL = 'http://10.171.224.66:5100/resumes/buy/'
SPIDER_MSG_USERNAME = 'runforever@163.com'
SPIDER_MSG_PASSWORD = '199o1113'

ON_LINE_TIME = datetime(
    year=2015, month=12, day=28, hour=19, minute=0, second=0)

MOBILE_REGISTER_LINK = 'http://m.pinbot.me/#/invite/'
