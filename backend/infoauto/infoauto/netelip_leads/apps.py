from django.apps import AppConfig


class NetelipLeadsAppConfig(AppConfig):

    name = "infoauto.netelip_leads"
    verbose_name = "Netelip Leads"

    def ready(self):
        try:
            import infoauto.netelip_leads.signals  # noqa F401
        except ImportError:
            pass

