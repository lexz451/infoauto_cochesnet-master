from django.apps import AppConfig


class NetelipAppConfig(AppConfig):

    name = "infoauto.netelip"
    verbose_name = "Netelip"

    def ready(self):
        try:
            import infoauto.netelip.signals  # noqa F401
        except ImportError:
            pass
