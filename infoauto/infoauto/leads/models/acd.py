# -*- coding: utf-8 -*-

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import CharField, FileField, BooleanField, DateTimeField, DurationField, ForeignKey, PROTECT
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from infoauto.leads.models.common import phone_regex
from infoauto.leads.models.concessionaires import Concessionaire
from infoauto.leads.models.leads import Lead


class ACD(TimeStampedModel):
    acd_remote_id = CharField(max_length=255, unique=True, help_text=_("Identificador único de la llamada"))
    orig_phone = CharField(validators=[phone_regex], max_length=17,
                           help_text=_("Numero de teléfono desde el que se ha llamado"))
    dest_phone = CharField(validators=[phone_regex], max_length=17,
                           help_text=_("Numero de teléfono al que se ha llamado"))
    acd_audio = FileField(null=True, blank=True, help_text=_("Fichero con el audio de la llamada"))
    acd_audio_link = CharField(max_length=255, blank=True, null=True, help_text=_("URL al fichero de la llamada"))
    answered_call = BooleanField(default=False, help_text=_("Llamada respondida"))
    date_contact = DateTimeField(blank=True, null=True, help_text=_("Fecha de contacto"))
    duration = DurationField(default=datetime.timedelta(), blank=True, null=True, help_text=_("Duración de la llamada"))
    lead = ForeignKey(Lead, on_delete=PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = _("ACD")
        verbose_name_plural = _("ACD's")

    @property
    def concession(self):
        try:
            instance = Concessionaire.objects.get(phones__number=self.dest_phone)
        except ObjectDoesNotExist:
            instance = None
        return instance

    @property
    def possible_leads(self):
        queryset = None
        if not self.lead:
            queryset = Lead.objects.filter(~Q(status='end'), client__phone=self.orig_phone).order_by("id").distinct()
        return queryset
