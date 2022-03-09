import datetime
from datetime import timezone

from django.db.models import ForeignKey, OneToOneField, CASCADE, PROTECT, SET_NULL, BooleanField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from infoauto.leads.models import Lead
from infoauto.leads.models.lead_management import LeadManagement, EVENT_INCOMING_CALL_KEY, EVENT_OUTCOMING_CALL_KEY
from infoauto.netelip.models import CallControlModel
from infoauto.users.models import User


class CallControlLeadModelHistoricalRecords(HistoricalRecords):
    pass


class CallControlLeadModel(TimeStampedModel):
    call_control = OneToOneField(CallControlModel, on_delete=CASCADE, null=True)
    lead = ForeignKey(Lead, on_delete=SET_NULL, blank=True, null=True)
    user = ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
    is_duplicated = BooleanField(default=False)
    history = CallControlLeadModelHistoricalRecords()

    def save(self, *args, **kwargs):

        # Comprobamos si es un duplicado.
        self.is_duplicated = self.get_is_duplicate()
        super().save(*args, **kwargs)

        # Actualizar métricas asociadas a llamadas en el LEAD.
        self.lead.update_call_metrics()


    def get_is_duplicate(self):
        # Si existe una asignación de lead-llamada con fecha más antigua y con origen un cliente,
        # significa que es un DUPLICADO.

        created = self.created
        if not created:
            created = datetime.datetime.now()

        return CallControlLeadModel.objects.filter(lead=self.lead, created__lt=created).exists()


    class Meta:
        verbose_name = _("Call & Lead Relation")
        verbose_name_plural = _("Call & Lead Relations")

