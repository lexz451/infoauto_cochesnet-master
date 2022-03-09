from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "infoauto.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import infoauto.users.signals  # noqa F401
        except ImportError:
            pass
