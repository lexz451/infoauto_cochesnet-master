# -*- coding: utf-8 -*-

import pytz
from django.conf import settings

from django.db.models import ManyToManyField, ForeignKey, CharField, TextField, PROTECT, DateTimeField, BooleanField, \
    FloatField, Q
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from infoauto.common.simple_history import HistoricalRecords
from infoauto.leads.models.lead_management import LeadManagement, EVENT_LEAD_CREATE_TRAKING_KEY, \
    EVENT_LEAD_CREATE_TASK_KEY, EVENT_LEAD_DONE_TRAKING_KEY, EVENT_LEAD_DONE_TASK_KEY

from infoauto.leads.models.notes import Note
from infoauto.leads.models.vehicles import Appraisal
from infoauto.users.models import User

TASK_TYPE = [
    # Para tareas
    ('date', _("Visita / Test Drive")),                                     # test drive            (comercial)
    ('appraisal', _("Appraisal")),                                          # appraisal              (comercial)
    ('budget', _('Budget')),                                                # presupuesto           (comercial)
    ('bono', _('Bono pedido')),                                             # bono perdido          (administrativa)
    ('insurance', _("Cotizar seguro")),                                     # cotizar seguro        (administrativa)
    ('financing', _('Financing')),                                          # financiación          (administrativa)
    ('service_contract', _('Contrato servicio')),                           # contrato servicio     (administrativa)
    ('vehicle_information', _('Información vehículo')),                     # información vehiculo  (comercial)
    ('send_catalog', _('Enviar catalogo')),                                 # enviar catalogo       (comercial)
    ('lost_call', _("Atender una llamada perdida")),                        # llamada perdida       (comercial)
    ('pre-delivery', _("Pre entrega vehículo")),                            # pre entrega vehículo  (administrativa)
    ('delivery', _("Entrega vehículo")),                                    # entrega vehículo      (comercial)
    ('campaign_mkt', _("Campaña MKT")),                                     # campana mkt           (comercial)
    ('renting', _("Renting")),                                              # campana mkt           (comercial)
    ('leasing', _("Leasing")),                                              # campana mkt           (comercial)
    # Para seguimiento
    ('ofert', _("Oferta")),                                                 # oferta                (comercial)
    ('program', _("Programada")),                                           # programada            (comercial)
    ('vehicle_arrival', _("Llegada vehiculo")),                             # llegada vehiculo      (comercial)
    ('campaign_mkt_tracing', _("Seguimiento Campaña MKT")),                 # campana mkt           (marketing)
    ('contact_7', _("Contacto 7 días")),                                    # contacto 7            (calidad)
    ('contact_60', _("Contacto 60 días")),                                  # contacto 60           (calidad)
    ('eqc_result', _("Resultado EQC")),                                     # resultado eqc         (calidad)
    # Para los dos
    ('other', _("Otros")),
    # No usados
    ('warranty', _('Warranty')),
    ('other', _("Otros")),
    ('response_information_mail', _("Respuesta a solicitud vía Email")),
    ('pending_assignment', _("Pendiente de asignación")),
    ('send_email', _("Enviar email")),
    ('workshop_appointment', _("Cita para taller")),
]



MEDIA = [
    ('Whatsapp', _('Whatsapp')),
    ('Phone', _('Phone')),
    ('SMS', _("SMS")),
    ('E-mail', _("E-mail")),
    ('face', _("Presencial"))
]

TASK_STATUS = [
    ('pending', _('Pending')),
    ('doing', _('Doing')),
    ('timeout', _('Timeout')),
    ('end', _('Finished')),
]


class HistoricalRecordsTask(HistoricalRecords):
    def post_save(self, instance, created, **kwargs):
        msg = None
        if created:
            msg = "La tarea '%s' ha sido dada de alta en el lead" % instance.get_type_display()
        elif self.get_changed_fields(sender=kwargs['sender'], instance=instance):
            msg = "La tarea '%s' ha sido modificada" % instance.get_type_display()
        return super().post_save(instance=instance, created=created, changeReason=msg, **kwargs)


class Task(TimeStampedModel):

    __original_realization_date_check = None

    author = ForeignKey(User, on_delete=PROTECT)
    type = CharField(choices=TASK_TYPE, max_length=255)
    subtype = CharField(max_length=255, blank=True, null=True)
    description = TextField(blank=True, null=True)
    media = CharField(choices=MEDIA, max_length=255, default='Phone')
    realization_date = DateTimeField(blank=True, null=True)
    tracking_date = DateTimeField(blank=True, null=True)
    note = ManyToManyField(Note, blank=True)
    appraisal = ForeignKey(Appraisal, on_delete=PROTECT, blank=True, null=True)
    realization_date_check = BooleanField(default=False)
    tracking_date_check = BooleanField(default=False)
    planified_realization_date = DateTimeField(blank=True, null=True)
    planified_tracking_date = DateTimeField(blank=True, null=True)
    is_click2call = BooleanField(default=False, help_text=_("Set True when tasks is created with button Click2Call"))
    id_call = FloatField(help_text=_("ID único de la llamada"), blank=True, null=True)
    is_traking_task = BooleanField(default=False)
    history = HistoricalRecordsTask()
    lead = ForeignKey('leads.Lead', on_delete=PROTECT, null=True, blank=True, related_name="tasks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_realization_date_check = self.realization_date_check

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def realization_date_changed(self):
        return bool(self.__original_realization_date_check != self.realization_date_check)


    @property
    def is_done(self):
        return self.realization_date is not None

    @property
    def date_literal(self):
        data_aux = None
        if self.realization_date_check and self.tracking_date_check:
            data = {'date': self.realization_date, 'text': "Realizada"}
        elif self.tracking_date_check:
            data = {'date': self.tracking_date, 'text': "Seguimiento realizado"}
            if self.planified_realization_date:
                data_aux = {'date': self.planified_realization_date, 'text': "Programada"}
        elif self.realization_date_check:
            data = {'date': self.realization_date, 'text': "Realizada"}
            if self.planified_tracking_date:
                data_aux = {'date': self.planified_tracking_date, 'text': "Seguimiento programado"}
        else:
            if (self.planified_realization_date and self.planified_tracking_date and
                    self.planified_realization_date <= self.planified_tracking_date):
                data = {'date': self.planified_realization_date, 'text': "Programada"}
            elif self.planified_realization_date and self.planified_tracking_date:
                data = {'date': self.planified_tracking_date, 'text': "Seguimiento programado"}
            else:
                if self.planified_tracking_date:
                    data = {'date': self.planified_tracking_date, 'text': "Seguimiento programado"}
                elif self.planified_realization_date:
                    data = {'date': self.planified_realization_date, 'text': "Programada"}
                else:
                    data = False
        date_list = []
        if data:
            data['date'] = data['date'].astimezone(
                pytz.timezone(settings.TIME_ZONE)
            ).strftime("%d-%m-%Y %H:%M")
            date_list = ["%(date)s" % data]
            if data_aux:
                data_aux['date'] = data_aux['date'].astimezone(
                    pytz.timezone(settings.TIME_ZONE)
                ).strftime("%d-%m-%Y %H:%M")
                txt_data_aux = ["%(date)s" % data_aux]
                date_list = txt_data_aux + date_list
        return date_list if data else []

    def save(self, *args, **kwargs):

        is_new = bool(self.pk is None)

        super().save(*args, **kwargs)
        self.change_lead_status()

        if self.lead:
            if is_new and self.is_traking_task:
                LeadManagement.objects.create(
                    lead_id=self.lead.id,
                    event=EVENT_LEAD_CREATE_TRAKING_KEY,
                    user=self.author,
                    status=self.lead.status,
                    message="Seguimiento programado: {0}".format(self.get_type_display())
                )
            elif is_new and not self.is_traking_task:
                LeadManagement.objects.create(
                    lead_id=self.lead.id,
                    event=EVENT_LEAD_CREATE_TASK_KEY,
                    user=self.author,
                    status=self.lead.status,
                    message="Tarea programada: {0}".format(self.get_type_display())
                )
            elif self.realization_date_changed() and self.is_traking_task:
                LeadManagement.objects.create(
                    lead_id=self.lead.id,
                    event=EVENT_LEAD_DONE_TRAKING_KEY,
                    user=self.author,
                    status=self.lead.status,
                    message="Seguimiento realizado: {0}".format(self.get_type_display())
                )
            elif self.realization_date_changed() and not self.is_traking_task:
                LeadManagement.objects.create(
                    lead_id=self.lead.id,
                    event=EVENT_LEAD_DONE_TASK_KEY,
                    user=self.author,
                    status=self.lead.status,
                    message="Tarea realizada: {0}".format(self.get_type_display())
                )

    def change_lead_status(self):

        """
        Si existe alguna tarea de tipo acción comercial, modifica el estado del lead, automaticamente.
        En caso de no existir tareas pendientes y existir alguna tarea de seguimiento, modifica el estado del
        lead a 'tracing'.
        """

        lead = self.lead
        if lead:

            any_task_not_done = lead.tasks.filter(is_traking_task=0, realization_date__isnull=True).exists()
            any_traking_not_done = lead.tasks.filter(is_traking_task=1, realization_date__isnull=True).exists()

            if any_task_not_done:
                self.lead.status = 'commercial_management'
                self.lead.save()

            elif any_traking_not_done:
                self.lead.status = 'tracing'
                self.lead.save()


class HistoricalRecordsRequest(HistoricalRecords):
    def post_save(self, instance, created, **kwargs):
        msg = None
        if created:
            msg = None
        if self.get_changed_fields(sender=kwargs['sender'], instance=instance) and not created:
            msg = "Tarea añadida"
        return super().post_save(instance=instance, created=created, changeReason=msg, **kwargs)


class Request(TimeStampedModel):
    task = ManyToManyField(Task, blank=True)
    history = HistoricalRecordsRequest()

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")

    @property
    def lead(self):
        queryset = self.lead_set.all()
        if queryset:
            return queryset[0]
        else:
            return None



















