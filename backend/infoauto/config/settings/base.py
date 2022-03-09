"""
Base settings to build other settings files upon.
"""
import os

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (infoauto/config/settings/base.py - 3 = infoauto/)
APPS_DIR = ROOT_DIR.path('infoauto')

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path('.env')))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'es-es'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#uLOCALE_PATHSse-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='mysql:///infoauto'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['OPTIONS'] = {
    "init_command": "SET foreign_key_checks = 0;",
}

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.humanize', # Handy template tags
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'rest_framework.authtoken',
    'simple_history',
    'channels',
    'django_celery_beat'
]
LOCAL_APPS = [
    'infoauto.taskapp.celery.CeleryAppConfig',
    'infoauto.users.apps.UsersAppConfig',
    'infoauto.countries.apps.CountryAppConfig',
    'infoauto.leads.apps.LeadsAppConfig',
    'infoauto.leads_public.apps.LeadsPublicAppConfig',
    'infoauto.work_calendar.apps.WorkCalendarAppConfig',
    'infoauto.tags_app.apps.TagAppConfig',
    'infoauto.source_channels.apps.SourceChannelAppConfig',
    'infoauto.click2call.apps.Click2CallAppConfig',
    'infoauto.sql_views.apps.SQLViewsAppConfig',
    'infoauto.netelip.apps.NetelipAppConfig',
    'infoauto.netelip_leads.apps.NetelipLeadsAppConfig',
    'infoauto.expanded_settings.apps.ExpandedSettingsAppConfig',
    'infoauto.actionlogging.apps.ActionLoggingAppConfig',
    'infoauto.chrome_extension.apps.ChromeExtensionAppConfig',
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {
    'sites': 'infoauto.contrib.sites.migrations'
}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'users:redirect'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'infoauto.users.middleware.LastActionUserMiddleware',
    'infoauto.actionlogging.middleware.ActionLoggingMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'admin/'
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Info Auto Admin""", 'infoauto.soporte@intelligenia.com'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = 'infoauto.users.adapters.AccountAdapter'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = 'infoauto.users.adapters.SocialAccountAdapter'


# Your stuff...
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # ~ 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter"
    ),
    'DEFAULT_PAGINATION_CLASS': 'infoauto.leads.apps.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
    "COERCE_DECIMAL_TO_STRING": False,
    "DATE_FORMAT": "%d/%m/%Y",
    "DATE_INPUT_FORMATS": ["%d/%m/%Y", "%d-%m-%Y"],
    "DATETIME_INPUT_FORMATS": [
        'iso-8601',
        '%d-%m-%Y',
        '%d-%m-%Y %H:%M:%S',
        '%d-%m-%Y %H:%M:%S.%f',
        '%d-%m-%Y %H:%M',
        '%d/%m/%Y',
        '%d/%m/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S.%f',
        '%d/%m/%Y %H:%M',
        '%Y-%m-%dT%H:%M:%S.%fZ'
    ]
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French'))
]

LOCALE_PATHS = (
    os.path.join(str(ROOT_DIR), 'locale'),
)

MIDDLEWARE += [
    'django.middleware.locale.LocaleMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

FORCE_ORIGIN = True

ALLOWED_TOKENS = []
# PRE
ALLOWED_TOKENS += ['c9a8c4c9bd6111b6cf877604edef70acebaac81e']
# PRO
ALLOWED_TOKENS += ['0a9c59ce4223c8846193981c113f8863e801222c']

# START - USER IS ONLINE
MIDDLEWARE += [
    'infoauto.users.middleware.ActiveUserMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 2 * 60 * 60   # 2 hours

# Number of seconds that we will keep track of inactive users for before
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7

AUTO_DISABLE_USER_TIME1_HOUR = 14
AUTO_DISABLE_USER_TIME1_MINUTE = 30

AUTO_DISABLE_USER_TIME2_HOUR = 20
AUTO_DISABLE_USER_TIME2_MINUTE = 30

# END - USER IS ONLINE

# Click2Call
URL_CLICK_2_CALL = "https://www.panelcliente.com/c2c/ws.php"
CLICK_2_CALL = {
    "accion": "solicitar",
    "idcliente": "77",
    "memberid": "",
    "telefono": ""
}

### NETELIP ####
NETELIP_API_NAME = "API 31c06"

# WebDAV
NETELIP_WEBDAV_URL = "http://vdrive.netelip.com/remote.php/webdav/"
NETELIP_WEBDAV_USER = "infodata"
NETELIP_WEBDAV_PASSWORD = "1qaz2wsx"
BASE_NETELIP_WEVDAV = {
    'webdav_hostname': NETELIP_WEBDAV_URL,
    'webdav_login': NETELIP_WEBDAV_USER,
    'webdav_password': NETELIP_WEBDAV_PASSWORD
}

NETELIP_SMS_URL = "https://api.netelip.com/v1/sms/api.php"
NETELIP_SMS_APITOKEN = "82649e945fb3ba0f6f60d28ea6a23159c018e4c1731ceb2b58cd4e4d0687a23f"

### NETELIP ###

# Channels
ASGI_APPLICATION = 'config.routing.application'
# channels-redis settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}


from .email_settings import *

MAIL_PUBLIC_RESPONSE = 'vomotorscoring@info-auto.es'

BASE_EMAIL_SLUG = 'email'
BASE_PHONE_SLUG = 'phone'
REQUIRED_SOURCE_DATA = [BASE_EMAIL_SLUG, BASE_PHONE_SLUG]

#  Celery
# # ------------------------------------------------------------------------------

if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = 'amqp://'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60

from .celery import *

SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True


# ACTIONLOGGING
# Varible que condiciona el almacenado de todas las llamadas a las vistas,
# si es False no almacenada nada en el log que no se indique de forma explicita en la vista
ACTIONLOGGING_SAVE_LOG = True

# Texto que se sustituye en los logs cuando queremos ocultar otro string
ACTIONLOGGING_TEXT_HIDE_REQUEST = "---HIDE---"
ACTIONLOGGING_TEXT_HIDE_RESPONSE = "---HIDE---"

# Campos a los que se les ofuscará el contenido
# HIDE_LOG_FIELDS = ["password","password1","password2","csrfmiddlewaretoken","base64"]
ACTIONLOGGING_FIELDS_HIDE_REQUEST = ["password","password1","password2","tradename"]
ACTIONLOGGING_FIELDS_HIDE_RESPONSE = ["password","password1","password2","tradename"]

# Lista de objetos url acción cuya LOGGING será ignorado [{"actions":["",""]|"","url":""},...]
ACTIONLOGGING_IGNORE_URL = [
        {'actions': ["GET","POST"], "url": "http://192.168.2.15:4422/api/pydrfpermissions/pydrfpermissions/"},
]

ACTIONLOGGING_ENABLE_URL = [
    {"actions": ["GET", "POST", "PUT", "PATCH", "DELETE"], "url": r'\/netelip\/'},
]

