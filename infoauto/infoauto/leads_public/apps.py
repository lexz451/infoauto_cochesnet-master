from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LeadsPublicAppConfig(AppConfig):

    name = "infoauto.leads_public"
    verbose_name = _("Leads Publicos")

