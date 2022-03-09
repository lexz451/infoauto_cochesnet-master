import environ


ROOT_DIR = environ.Path(__file__) - 3
env = environ.Env()
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR.path('.env')))


DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL',
    default='HandsfreeCRM <noreply@example.com>'
)
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "procesos@info-auto.es"
EMAIL_HOST_PASSWORD = "smartmotorlead@"
EMAIL_USE_TLS = True

# lead_user_asign
NL_EMAIL_HOST_USER = "vomotorscoring@info-auto.es"
NL_EMAIL_HOST_PASSWORD = "smartmotorlead@@"

SMTP_CONFIG = {
    "default": {
        "host": EMAIL_HOST,
        "port": EMAIL_PORT,
        "username": EMAIL_HOST_USER,
        "password": EMAIL_HOST_PASSWORD,
        "use_tls": EMAIL_USE_TLS
    },
    "lead_user_assign": {
        "host": EMAIL_HOST,
        "port": EMAIL_PORT,
        "username": NL_EMAIL_HOST_USER,
        "password": NL_EMAIL_HOST_PASSWORD,
        "use_tls": EMAIL_USE_TLS,
        "from_email": "Alertas Smart Motor Lead <%s>" % NL_EMAIL_HOST_USER
    }
}

EMAILS_FORGOTTEN_CALL = [NL_EMAIL_HOST_USER, 'sclemente@info-auto.es']
