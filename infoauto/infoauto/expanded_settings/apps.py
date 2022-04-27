from django.apps import AppConfig


class ExpandedSettingsAppConfig(AppConfig):

    name = "infoauto.expanded_settings"
    verbose_name = "Expanded Settings"

    def ready(self):
        try:
            import infoauto.expanded_settings.signals
        except ImportError:
            pass
