from .base import *  # noqa
from .base import env
import os

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
#SECRET_KEY = env('DJANGO_SECRET_KEY')
DJANGO_SECRET_KEY = 'tha3vahrahmae8EeJei7ohzaev9chu'
SECRET_KEY = DJANGO_SECRET_KEY
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
#ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['http://krart.testing.intelligenia.com'])
#ALLOWED_HOSTS = ['localhost','smartmotorlead.net', 'www.smartmotorlead.net', 'crmcochesnet.info-auto.es', 'sail.artificialintelligencelead.com']
ALLOWED_HOSTS = ['*']
DEBUG = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa F405

# DATABASES
# ------------------------------------------------------------------------------

DATABASES['default']['ATOMIC_REQUESTS'] = True  # noqa F405
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # noqa F405

DATABASES['default']['NAME'] = env('MYSQL_DATABASE')
DATABASES['default']['USER'] = env('MYSQL_USER')
DATABASES['default']['PASSWORD'] = env('MYSQL_PASSWORD')
DATABASES['default']['HOST'] = env('MYSQL_HOST')

#DATABASES['default']['DATABASE_URL'] = "mysql:///localhost:3306"
#DATABASES['default']['ENGINE'] = "sql_server.pyodbc"
#DATABASES['default']['NAME'] = "crmcochesnet_info_auto_es"
#DATABASES['default']['USER'] = "crmcochesnet_infoauto"
#DATABASES['default']['PASSWORD'] = "pohshariethu5Ei"
#DATABASES['default']['HOST'] = "10.8.0.6"
#DATABASES['default']['PORT'] = "1433"
#DATABASES['default']['OPTIONS'] = { 'driver': 'ODBC Driver 17 for SQL Server' }


# CACHES
# ------------------------------------------------------------------------------
#CACHES = {
#    'default': {
#        'BACKEND': 'django_redis.cache.RedisCache',
#        'LOCATION': env('REDIS_URL'),
#        'OPTIONS': {
#            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
#            'IGNORE_EXCEPTIONS': True,
#        }
#    }
#}

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'


# STATIC
# ------------------------

#STATIC_URL = "/static/"
#STATIC_ROOT = os.path.join(str(ROOT_DIR), 'public_html/collectedstatic')

# MEDIA
# ------------------------------------------------------------------------------


# endregion
#MEDIA_URL = "/media/"
#MEDIA_ROOT = "/var/www/crmcochesnet.info-auto.es/backend/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
#TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
#    (
#        'django.template.loaders.cached.Loader',
#        [
#            'django.template.loaders.filesystem.Loader',
#            'django.template.loaders.app_directories.Loader',
#        ]
#    ),
#]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL',
    default='sail <noreply>'
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[SAIL]')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
#ADMIN_URL = env('DJANGO_ADMIN_URL')

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
#INSTALLED_APPS += ['anymail']  # noqa F405
#EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
#ANYMAIL = {
#    'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
#    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_DOMAIN')
#}

# Gunicorn
# ------------------------------------------------------------------------------
#INSTALLED_APPS += ['gunicorn',]  # noqa F405

# Collectfast
# ------------------------------------------------------------------------------
# https://github.com/antonagestam/collectfast#installation
#INSTALLED_APPS = ['collectfast'] + INSTALLED_APPS  # noqa F405
#AWS_PRELOAD_METADATA = True


# LOGGING
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}


# Your stuff...
# ------------------------------------------------------------------------------
#CELERY_BROKER_URL = 'amqp://crmcochesnet:Jeimo5aishiezie@localhost:5672//crmcochesnet'
#CELERY_RESULT_BACKEND = CELERY_BROKER_URL

REDIS_HOST = env('REDIS_URL')
CELERY_BROKER_URL = REDIS_HOST
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('redis', 6379)],
        },
    },
}

ALLOWED_TOKENS += ['c9a8c4c9bd6111b6cf877604edef70acebaac81e']
