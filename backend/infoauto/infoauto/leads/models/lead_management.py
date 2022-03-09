from model_utils.models import TimeStampedModel
from django.db import models

from django.utils.translation import gettext_lazy as _

from infoauto.common.util_email import send_email
from infoauto.netelip.sms import send_sms, NetelipSMSException
from infoauto.users.models import UserSFA

CHANNEL_EMAIL_KEY = "email"
CHANNEL_SMS_KEY = "sms"


EVENT_LEAD_NOT_ATTENDED_KEY = "lead_not_attended"
EVENT_LEAD_ATTENDED_KEY = "lead_attended"
EVENT_LEAD_END_KEY = "lead_end"
EVENT_LEAD_REACTIVATED_KEY = "lead_reactivated"
EVENT_LEAD_CREATE_TASK_KEY = "lead_create_task"
EVENT_LEAD_DONE_TASK_KEY = "lead_done_task"
EVENT_LEAD_CREATE_TRAKING_KEY = "lead_create_traking"
EVENT_LEAD_DONE_TRAKING_KEY = "lead_done_traking"
EVENT_INCOMING_CALL_KEY = "incoming_all"
EVENT_OUTCOMING_CALL_KEY = "outcomming_all"
EVENT_OUTCOMING_WHATSAPP_KEY = "outcomming_all"
EVENT_CHANGE_USER = "change_user"


EVENTS_OPTS = [
    (EVENT_LEAD_NOT_ATTENDED_KEY, _('Lead no atendido')),
    (EVENT_LEAD_ATTENDED_KEY, _('Lead atendido')),
    (EVENT_LEAD_END_KEY, _('Lead finalizado')),
    (EVENT_LEAD_REACTIVATED_KEY, _('Lead reactivado')),
    (EVENT_LEAD_CREATE_TASK_KEY, _('Nueva tarea creada en lead')),
    (EVENT_LEAD_DONE_TASK_KEY, _('Tarea finalizada en lead')),
    (EVENT_LEAD_CREATE_TRAKING_KEY, _('Nuevo seguimiento en lead')),
    (EVENT_LEAD_DONE_TRAKING_KEY, _('Seguimiento finalizado en lead')),
    (EVENT_INCOMING_CALL_KEY, _('Llamada entrante en lead')),
    (EVENT_OUTCOMING_CALL_KEY, _('Llamada saliente en lead')),
    (EVENT_OUTCOMING_WHATSAPP_KEY, _('WhatsApp enviado')),
    (EVENT_CHANGE_USER, _('Cambio de asignacion')),
]


class LeadManagement(TimeStampedModel):
    lead = models.ForeignKey('leads.Lead', on_delete=models.CASCADE, related_name="lead_managements")
    event = models.CharField(max_length=224, choices=EVENTS_OPTS, null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.emit_event_alert()

    def emit_event_alert(self):
        if not LeadManagement.objects.filter(lead=self.lead, event=self.event, user=self.user).exclude(id=self.id).exists():
            user_related_sfa_set = UserSFA.objects.filter(user=self.user, event=self.event)
            for user_related_sfa in user_related_sfa_set:
                if user_related_sfa.channel == CHANNEL_EMAIL_KEY and self.lead.client.email:
                    try:
                        send_email(
                            to_email=[self.lead.client.email],
                            subject=self.lead.concessionaire.name,
                            template='email/alert_lead',
                            context={'message': user_related_sfa.text},
                            smtp_config_name="default"
                        )
                    except:
                        print("[ERROR] No se envian email")

                elif user_related_sfa.channel == CHANNEL_SMS_KEY and self.lead.client.mobile:
                    try:
                        send_sms(
                            from_sms=self.lead.user.phone,
                            destination_sms=self.lead.client.mobile,
                            message_sms=user_related_sfa.text
                        )
                    except NetelipSMSException as e:
                        print("[ERROR] " + str(e))
