# -*- coding: utf-8 -*-

import datetime
from django.db import models

from django.apps import apps
from django.db.models import TextField, CharField, EmailField, ForeignKey, DateTimeField, CASCADE, PROTECT, \
    ManyToManyField, Q, SET_NULL, BooleanField, DurationField, PositiveIntegerField, DO_NOTHING
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords as OriginalHistoricalRecords

from infoauto.common.simple_history import HistoricalRecords
from infoauto.common.util_phone import normalize_phone
from infoauto.leads.models.lead_management import LeadManagement, EVENT_LEAD_END_KEY, EVENT_LEAD_ATTENDED_KEY, \
    EVENT_LEAD_REACTIVATED_KEY, EVENT_OUTCOMING_WHATSAPP_KEY, EVENT_CHANGE_USER
from infoauto.leads.models.notes import Note
from infoauto.leads.models.clients import Client
from infoauto.leads.models.common import phone_regex
from infoauto.leads.models.concessionaires import Concessionaire, Phone, Email
from infoauto.leads.models.tasks import Request, Task
from infoauto.leads.models.vehicles import Vehicle
from infoauto.leads.models.comment import Comment
from infoauto.source_channels.models import Source, Channel
from infoauto.tags_app.models import Tag

from infoauto.users.models import User, EVENT_LEAD_NOT_ATTENDED_KEY

SCORE_CHOICES = [
    ('1', _("Very low")),
    ('2', _("Low")),
    ('3', _("Medium")),
    ('4', _("High"))
]

LEAD_STATUS_NEW = "new"
LEAD_STATUS_ATTENDED = "attended"
LEAD_STATUS_PENDING = "pending"
LEAD_STATUS_COMMERCIAL_MANAGEMENT = "commercial_management"
LEAD_STATUS_TRACING = "tracing"
LEAD_STATUS_END = "end"

LEAD_STATUS = [
    (LEAD_STATUS_NEW, _('new opportunity')),
    (LEAD_STATUS_ATTENDED, _('Attended')),
    (LEAD_STATUS_PENDING, _('Pending')),
    (LEAD_STATUS_COMMERCIAL_MANAGEMENT, _("Commercial management")),
    (LEAD_STATUS_TRACING, _("Tracing")),
    (LEAD_STATUS_END, _("End"))
]

LEAD_RESULT = [
    ('not_available', _("No disponible")),
    ('negative', _("Descartado")),
    ('reserved_vehicle', _("Vehicle reserved")),
    ('positive', _("Ganado")),
    ('unreachable', _("Unreachable")),
    ('wrong', _("Duplicado")),
    ('error', _("Error")),
]

LEAD_RESULT_REASON = [
    # Para negativo
    ('rechaza_financiacion', _("Rechaza financiación")),
    ('rechaza_tasacion', _("Rechaza tasación")),
    ('rechaza_precio', _("Rechaza precio")),
    ('aplaza_compra', _("Aplaza compra")),
    ('compra_competencia', _("Compra competencia")),
    # Para negativo V2
    ('compra_competencia_precio', _("Compra competencia por precio")),
    ('compra_competencia_proximidad', _("Compra competencia por proximidad")),
    ('compra_competencia_stock', _("Compra competencia por stock")),
    ('infinanciable', _("Infinanciable")),
    ('aplaza_decision', _("Aplaza decisión")),
    ('otro', _("Otro")),
    ('duplicado', _("Duplicado")),
    ('cita_cancelada', _("Cita cancelada")),
    ('informacion_cliente_incorrecta', _("Información cliente incorrecta")),
    ('ilocalizable', _("Ilocalizable")),
    ('disconforme_tasacion', _("Disconforme con tasación")),
    ('caducado', _("Caducado")),
    ('no_encaja_producto', _("No le encaja el producto")),
    ('no_encaja_precio', _("No le encaja el precio")),
    ('no_encaja_cuota', _("No le encaja la cuota")),
    ('vehiculo_ya_vendido', _("Vehiculo ya vendido")),

    # Para no disponible
    ('pre-reservado', _("Pre-Reservado")),
    ('reservado', _("Reservado")),
    # Para error
    ('publicidad', _("Publicidad")),
    ('otro_departamento', _("Otro Departamento")),
    ('error', _("Error")),
    # para positivo
    ('pedido', _("Pedido")),
    ('reservado', _("Reservado")),
]

STATUS_CALL = [
    ('undefined', 'Desconocido'),
    ('attended', 'Atendida'),
    ('not_attended', 'No atendida'),
    ('out_of_working_hours', 'Fuera de horario laboral'),
]

REQUEST_TYPE_CHOICES = [
    ('new', _("Nuevo")),
    ('used', _("Ocasión")),
    ('km0', _("Kilometro 0")),
    ('management', _("Gerencia")),
    ('seminew', _("Seminuevo")),
    ('apv', _("Postventa")),
    ('acc', _("Accesorios")),
]

INTEGRATED = "integrated"
NOT_INTEGRATED = "not_integrated"
NOT_HBS_API_KEY = "not_api_key"


class HistoricalRecordsLead(HistoricalRecords):
    created = None
    mapped_field_names = {
        'vehicle': "VEHÍCULO",
        'score': "SCORE",
        'note': "NOTAS",
        'client': "CLIENTE",
        'tags': "TAGS",
        'status': "ESTADO",
    }

    def post_save(self, instance, created, **kwargs):
        self.created = created
        msg = None
        changed_fields = self.get_changed_fields(sender=kwargs['sender'], instance=instance)
        if created:
            msg = "El lead ha sido dado de alta en el sistema"
        elif changed_fields:
            field_names = []
            for i in changed_fields:
                if self.mapped_field_names.get(i['field'].name):
                    field_names.append(self.mapped_field_names[i['field'].name])
            msg = "El lead ha sido modificado. " \
                  "Las secciones afectadas son las siguientes: <br>" \
                  "%s" % ', '.join(field_names)
        return super().post_save(instance=instance, created=created, changeReason=msg, **kwargs)

    def create_historical_record(self, instance, history_type):
        if self.created:
            setattr(instance, '_history_date', now() - datetime.timedelta(seconds=1))
        return super().create_historical_record(instance, history_type)


class Lead(TimeStampedModel):
    __original_status = None

    concession_phone = CharField(validators=[phone_regex], max_length=17, help_text=_("Phone"), blank=True, null=True)
    concession_email = EmailField(blank=True, null=True, help_text=_("Email de concesión"))
    status = CharField(max_length=255, choices=LEAD_STATUS, default='new')

    client = ForeignKey(Client, on_delete=SET_NULL, blank=True, null=True)
    request = ForeignKey(Request, on_delete=CASCADE, null=True)

    end_date = DateTimeField(blank=True, null=True)
    user = ForeignKey(User, on_delete=PROTECT, blank=True, null=True)
    assigned_date = DateTimeField(default=None, null=True)
    concessionaire = ForeignKey(Concessionaire, on_delete=CASCADE)
    result = CharField(choices=LEAD_RESULT, max_length=255, blank=True, null=True)
    result_reason = CharField(choices=LEAD_RESULT_REASON, max_length=255, blank=True, null=True)
    result_comments = TextField(blank=True, null=True, default='')
    request_type = CharField(max_length=255, choices=REQUEST_TYPE_CHOICES, blank=True, null=True)
    request_notes = TextField(blank=True, null=True)

    finish_date = DateTimeField(blank=True, null=True)
    note = ManyToManyField(Note, blank=True)
    comments = ManyToManyField(Comment, blank=True)
    score = CharField(max_length=255, choices=SCORE_CHOICES, blank=True, null=True)
    mail_content = TextField(blank=True, null=True)
    lead_task_date = DateTimeField(blank=True, null=True, help_text=_("Keep first task date to do. "
                                                                      "Needed for making date filters on leads grid"))
    tags = ManyToManyField(Tag, blank=True)
    source = ForeignKey(Source, blank=True, null=True, on_delete=PROTECT)
    source2 = CharField(max_length=255, blank=True, null=True)

    origin2 = ForeignKey("Origin", null=True, on_delete=SET_NULL)
    channel2 = ForeignKey(Channel, null=True, on_delete=SET_NULL)

    psa_id = CharField(max_length=255, blank=True, null=True)

    history = HistoricalRecordsLead()

    # Status dates
    status_new_datetime = DateTimeField(blank=True, null=True)
    status_pending_datetime = DateTimeField(blank=True, null=True)
    status_attended_datetime = DateTimeField(blank=True, null=True)
    status_tracing_datetime = DateTimeField(blank=True, null=True)
    status_end_datetime = DateTimeField(blank=True, null=True)

    # Custom status dates
    custom_status_new_datetime = DateTimeField(blank=True, null=True)
    custom_status_pending_datetime = DateTimeField(blank=True, null=True)
    custom_status_attended_datetime = DateTimeField(blank=True, null=True)
    custom_status_tracing_datetime = DateTimeField(blank=True, null=True)
    custom_status_end_datetime = DateTimeField(blank=True, null=True)

    # Reactivated lead, fields.
    is_reactivated = BooleanField(default=False)
    reactivated_date = DateTimeField(blank=True, null=True)
    before_reactivated_finish_date = DateTimeField(blank=True, null=True)
    before_reactivated_result = CharField(choices=LEAD_RESULT, max_length=255, blank=True, null=True)

    # Call fields.
    incoming_call_datetime = DateTimeField(blank=True, null=True)
    status_call = CharField(max_length=224, null=True, blank=True, choices=STATUS_CALL)
    outgoing_call_datetime = DateTimeField(blank=True, null=True)

    # Email fields.
    incoming_email_datetime = DateTimeField(blank=True, null=True)
    outgoing_email_datetime = DateTimeField(blank=True, null=True)

    # Computed ASA
    computed_call_asa = PositiveIntegerField(blank=True, null=True)
    computed_email_asa = PositiveIntegerField(blank=True, null=True)

    threshold_concession_call = PositiveIntegerField(default=3600)  # Workaround
    threshold_concession_email = PositiveIntegerField(default=7200)  # Workaround

    is_imported = BooleanField(default=False)

    # HubSpot integration status
    hubspot_status = BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__last_user = self.user
        self.__original_status = self.status

    def status_changed(self):
        return bool(self.status != self.__original_status)

    def save(self, *args, **kwargs):

        new_user = False
        is_new = self.id is None
        self.change_lead_status()

        if is_new:
            if self.user is not None:
                self.assigned_date = timezone.now()
        else:
            prev = Lead.objects.get(id=self.id)
            if prev.user != self.user:
                self.assigned_date = timezone.now()
                new_user = True

        self.concession_phone = normalize_phone(self.concession_phone)

        super().save(*args, **kwargs)

        self.update_status_metrics()
        self.update_call_metrics()

        if is_new:
            LeadManagement.objects.create(
                lead_id=self.id,
                event=EVENT_LEAD_NOT_ATTENDED_KEY,
                user=self.user,
                status=self.status,
                message="Lead ha sido dado de alta en el sistema"
            )
        elif self.status_changed() and self.status == LEAD_STATUS_END:
            LeadManagement.objects.create(
                lead_id=self.id,
                event=EVENT_LEAD_END_KEY,
                user=self.user,
                status=self.status,
                message="Lead cerrado"
            )
        elif self.status_changed() and self.status == LEAD_STATUS_ATTENDED:
            LeadManagement.objects.create(
                lead_id=self.id,
                event=EVENT_LEAD_ATTENDED_KEY,
                user=self.user,
                status=self.status,
                message="Lead ha sido atendido"
            )

        if new_user:
            LeadManagement.objects.create(
                lead_id=self.id,
                event=EVENT_CHANGE_USER,
                user=self.user,
                status=self.status,
                message="Lead ha sido asignado a otra persona"
            )

    def change_lead_status(self):

        """
        Si existe alguna tarea de tipo acción comercial, modifica el estado del lead, automaticamente.
        En caso de no existir tareas pendientes y existir alguna tarea de seguimiento, modifica el estado del
        lead a 'tracing'.
        """

        any_task_not_done = self.tasks.filter(is_traking_task=0, realization_date_check=False).exists()
        any_traking_not_done = self.tasks.filter(is_traking_task=1, realization_date_check=False).exists()

        # commercial_management_task = self.tasks.filter(
        #     is_traking_task=0, realization_date_check=False
        # ).filter(
        #     Q(type='lost_call') | Q(type='other')
        # ).exists()

        if any_task_not_done:
            self.status = 'commercial_management'

        elif any_traking_not_done:
            self.status = 'tracing'

    class Meta:
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")

    def get_computed_call_asa(self):
        if self.incoming_calls and self.outgoing_calls:
            incoming_call = self.incoming_calls.first()
            outgoing_call = self.outgoing_calls.first()

            self.computed_call_asa = (
                    incoming_call.call_control.startcall - outgoing_call.call_control.startcall).seconds
            return self.computed_call_asa

    def get_computed_email_asa(self):
        self.computed_email_asa = 0
        return self.computed_email_asa

    #########################################################################################################
    #########################################################################################################

    def get_status_new_datetime(self):
        if self.status_new_datetime is None:
            if self.custom_status_new_datetime:
                self.status_new_datetime = self.custom_status_new_datetime
            else:
                if self.status == 'new':
                    self.status_new_datetime = self.modified

                else:
                    status_new_history = self.history.filter(status='new').order_by('history_id').first()
                    if status_new_history:
                        self.status_new_datetime = status_new_history.history_date

            Lead.objects.filter(id=self.id).update(status_new_datetime=self.status_new_datetime)

    def get_status_pending_datetime(self):
        if self.status_pending_datetime is None:
            if self.custom_status_pending_datetime:
                self.status_pending_datetime = self.custom_status_pending_datetime
            else:
                if self.status == 'commercial_management':
                    self.status_pending_datetime = self.modified
                else:
                    status_pending_history = self.history.filter(status='commercial_management').order_by(
                        'history_id').first()
                    if status_pending_history:
                        self.status_pending_datetime = status_pending_history.history_date

            Lead.objects.filter(id=self.id).update(status_pending_datetime=self.status_pending_datetime)

    def get_status_attended_datetime(self):
        if self.status_attended_datetime is None:
            if self.custom_status_attended_datetime:
                self.status_attended_datetime = self.custom_status_attended_datetime
            else:
                if self.status == 'attended':
                    self.status_attended_datetime = self.modified
                else:
                    status_attended_history = self.history.filter(status='attended').order_by('history_id').first()
                    if status_attended_history:
                        self.status_attended_datetime = status_attended_history.history_date

            Lead.objects.filter(id=self.id).update(status_attended_datetime=self.status_attended_datetime)

    def get_status_tracing_datetime(self):
        if self.status_tracing_datetime is None:
            if self.custom_status_tracing_datetime:
                self.status_tracing_datetime = self.custom_status_tracing_datetime
            else:
                if self.status == 'tracing':
                    self.status_tracing_datetime = self.modified
                else:
                    status_tracing_history = self.history.filter(status='tracing').order_by('history_id').first()
                    if status_tracing_history:
                        self.status_tracing_datetime = status_tracing_history.history_date

            Lead.objects.filter(id=self.id).update(status_tracing_datetime=self.status_tracing_datetime)

    def get_status_end_datetime(self):
        if self.status_end_datetime is None:
            if self.custom_status_end_datetime:
                self.status_end_datetime = self.custom_status_end_datetime
            else:
                if self.status == 'end':
                    self.status_end_datetime = self.modified
                else:
                    status_end_history = self.history.filter(status='end').order_by('history_id').first()
                    if status_end_history:
                        self.status_end_datetime = status_end_history.history_date

            Lead.objects.filter(id=self.id).update(status_end_datetime=self.status_end_datetime)

    def update_status_metrics(self):
        self.get_status_new_datetime()
        self.get_status_pending_datetime()
        self.get_status_attended_datetime()
        self.get_status_tracing_datetime()
        self.get_status_end_datetime()

    #########################################################################################################
    #########################################################################################################

    def get_incoming_email_datetime(self):
        self.incoming_email_datetime = datetime.datetime.now()  # TODO
        Lead.objects.filter(id=self.id).update(incoming_email_datetime=datetime.datetime.now())
        return self.incoming_email_datetime

    def get_outgoing_email_datetime(self):
        self.outgoing_email_datetime = datetime.datetime.now()  # TODO
        Lead.objects.filter(id=self.id).update(outgoing_email_datetime=datetime.datetime.now())
        return self.outgoing_email_datetime

    def update_email_metrics(self):
        # TODO
        self.get_incoming_email_datetime()
        self.get_outgoing_email_datetime()

    #########################################################################################################
    #########################################################################################################

    @property
    def incoming_calls(self):
        from infoauto.netelip_leads.models import CallControlLeadModel
        return CallControlLeadModel.objects.filter(lead=self, call_control__call_origin='client')

    @property
    def outgoing_calls(self):
        from infoauto.netelip_leads.models import CallControlLeadModel
        return CallControlLeadModel.objects.filter(lead=self, call_control__call_origin='user')

    def get_incoming_call_datetime(self):
        incoming_call = self.incoming_calls.first()

        if incoming_call:
            self.incoming_call_datetime = incoming_call.call_control.startcall
            Lead.objects.filter(id=self.id).update(incoming_call_datetime=incoming_call.call_control.startcall)
            return self.incoming_call_datetime

    def get_outgoing_call_datetime(self):
        outgoing_call = self.outgoing_calls.first()
        if outgoing_call:
            self.outgoing_call_datetime = outgoing_call.call_control.startcall
            Lead.objects.filter(id=self.id).update(outgoing_call_datetime=outgoing_call.call_control.startcall)
            return self.outgoing_call_datetime

    def get_call_status(self):

        """
        :return: STATUS_CALL = [
            ('attended', 'Atendida'),
            ('not_attended', 'No atendida'),
            ('out_of_working_hours', 'Fuera de horario laboral'),
        ]
        """

        ten_seconds = datetime.timedelta(seconds=10)

        afternoon_start_break = datetime.time(14, 0)
        afternoon_end_break = datetime.time(16, 0)
        night_start_break = datetime.time(21, 0)
        night_end_break = datetime.time(9, 0)

        if not self.incoming_calls.exists():
            self.status_call = 'undefined'

        else:
            call_attended = self.incoming_calls.filter(
                call_control__statuscall__in=('Connected', 'ANSWER')
            ).exists()

            if call_attended:
                self.status_call = 'attended'

            elif self.incoming_calls.filter(
                    call_control__startcall_time__gte=afternoon_start_break,
                    call_control__startcall_time__lte=afternoon_end_break
            ).exists():
                self.status_call = 'out_of_working_hours'

            elif self.incoming_calls.filter(call_control__startcall_time__gte=night_start_break).exists() \
                    or self.incoming_calls.filter(call_control__startcall_time__lte=night_end_break).exists():
                self.status_call = 'out_of_working_hours'
            else:
                self.status_call = 'not_attended'

        Lead.objects.filter(id=self.id).update(status_call=self.status_call)
        return self.status_call

    def update_call_metrics(self):
        self.get_incoming_call_datetime()
        self.get_outgoing_call_datetime()
        self.get_call_status()
        self.get_computed_call_asa()

    #########################################################################################################
    #########################################################################################################

    @property
    def last_lead_action(self):
        return self.leadaction_set.all().order_by('id').last()

    @property
    def last_lead_action_update(self):
        date_now = datetime.datetime.now()
        return self.leadaction_set.filter(date__lte=date_now).order_by('date', 'id').last()

    @property
    def channel(self):
        return self.source.channel.slug if self.source.channel else None

    @property
    def pending_tasks(self):
        query = Q(realization_date_check=False) | Q(tracking_date_check=False)
        if not self.request.task.all() or self.request.task.filter(query):
            return True
        return False

    @property
    def pending_tasks_count(self):
        return self.request.task.filter(realization_date_check=False).count()

    @property
    def done_tasks_count(self):
        return self.request.task.filter(realization_date_check=True).count()

    @property
    def sent_whatsapp_count(self):
        return self.whatsappmessage.all().count()

    @property
    def sent_emails_count(self):
        return self.lead_managements.filter(message='Email enviado').count()

    @property
    def sent_phone_call_count(self):
        return self.outgoing_calls.count()

    @property
    def task_count(self):
        return self.tasks.filter(is_traking_task=False, realization_date_check=True).count()

    @property
    def tracking_count(self):
        return self.tasks.filter(is_traking_task=True, realization_date_check=True).count()

    def reactivate(self):
        if self.status == LEAD_STATUS_END:
            # Copy old information in reactivated fields-
            self.is_reactivated = True
            self.reactivated_date = datetime.datetime.now()
            self.before_reactivated_result = self.result
            self.before_reactivated_finish_date = self.finish_date

            # Reset fields.
            self.result = None
            self.finish_date = None
            self.status = LEAD_STATUS_COMMERCIAL_MANAGEMENT

            self.save()

            LeadManagement.objects.create(
                lead_id=self.id,
                event=EVENT_LEAD_REACTIVATED_KEY,
                user=self.user,
                status=self.status,
                message="Lead reactivado"
            )

    def task_date(self, save_instance=True):
        queryset = self.request.task.filter(is_traking_task=False)
        first_tracking_date = None
        fist_realization_date = None
        ftd = queryset.filter(planified_tracking_date__isnull=False, tracking_date_check=False) \
            .order_by("planified_tracking_date").first()
        if ftd:
            first_tracking_date = ftd.planified_tracking_date
        frd = queryset.filter(planified_realization_date__isnull=False, realization_date_check=False) \
            .order_by("planified_realization_date").first()
        if frd:
            fist_realization_date = frd.planified_realization_date
        if first_tracking_date and fist_realization_date and (first_tracking_date < fist_realization_date):
            date_keep = first_tracking_date
        elif first_tracking_date and fist_realization_date and (first_tracking_date > fist_realization_date):
            date_keep = fist_realization_date
        elif first_tracking_date:
            date_keep = first_tracking_date
        elif fist_realization_date:
            date_keep = fist_realization_date
        else:
            instance = queryset.filter(realization_date_check=True, realization_date__isnull=False) \
                .order_by("realization_date").last()
            if instance:
                date_keep = instance.realization_date
            else:
                date_keep = self.created
        if save_instance:
            self.lead_task_date = date_keep
            self.save()
        return date_keep

    @property
    def first_task_date(self):
        return self.task_date(save_instance=False)

    @property
    def first_tracking_task(self):
        ttask = self.request.task.all().order_by('-tracking_date').first()
        if ttask:
            return ttask.tracking_date

    @property
    def last_tracking_task(self):
        ttask = self.request.task.all().order_by('tracking_date').first()
        if ttask:
            return ttask.tracking_date

    @property
    def last_realization_task(self):
        ttask = self.request.task.all().order_by('realization_date').first()
        if ttask:
            return ttask.realization_date

    @property
    def nsa(self):
        if self.lead_task_date and self.created:
            difference = self.lead_task_date - self.created
            seconds = difference.total_seconds()
            seconds = 0 if seconds < 0 else seconds
            d = datetime.datetime(1, 1, 1) + datetime.timedelta(seconds=seconds)
            return {
                'years': d.year - 1, 'months': d.month - 1,
                'days': d.day - 1, 'hours': d.hour,
                'minutes': d.minute, 'seconds': d.second
            }
        else:
            return None

    @property
    def origin(self):
        return self.get_origin()

    def get_origin(self):
        """
        origin = None
        if self.concession_phone:
            try:
                origin = Phone.objects.get(number=self.concession_phone).origin
            except Phone.DoesNotExist:
                pass
        elif self.concession_email:
            try:
                origin = Email.objects.get(email=self.concession_email).origin
            except Email.DoesNotExist:
                pass
        """
        return self.source.origin if self.source else None

    #########################################################################################################
    #########################################################################################################

    @property
    def hubspot_integration_status(self):
        """
        Check if HubSpot is synchronized or concessionaire has api key for HubSpot.
        """
        if self.hubspot_status:
            return INTEGRATED
        else:
            if self.concessionaire.hubspot_api_key:
                return NOT_INTEGRATED
            else:
                return NOT_HBS_API_KEY


NORMAL_KEY = 'normal'
WARNING_KEY = 'warning'
IMMEDIATE_KEY = 'immediate'
DONE_KEY = 'done'

ACTION_STATUS = (
    (NORMAL_KEY, _("Normal")),
    (WARNING_KEY, _("Alerta")),
    (IMMEDIATE_KEY, _("Urgente")),
    (DONE_KEY, _('Realizada')),
)

LEAD_STATUS_PLANING = [
    ('new', _("Nuevo")),
    ('commercial_management', _("Commercial management")),
    ('tracing', _("Tracing")),
    ('attended', _("Attended")),
    ('end', _("Closed"))
]


class HistoricalRecordsLeadAction(OriginalHistoricalRecords):
    pass


class LeadAction(TimeStampedModel):
    lead = ForeignKey(Lead, on_delete=CASCADE, help_text=_("Lead asociado"))
    history_lead = ForeignKey('HistoricalLead', on_delete=CASCADE, editable=False,
                              help_text=_("Captura la copia de la instancia en el instante de creación"))
    history_tasks = ManyToManyField('leads.HistoricalTask', blank=True)
    lead_status_planing = CharField(choices=LEAD_STATUS_PLANING, max_length=255,
                                    help_text=_("Estado esperado en la próxima actuación"))
    date = DateTimeField(help_text=_("Fecha de planificación de actuación"))
    status = CharField(choices=ACTION_STATUS, max_length=255, help_text=_("Estado de urgencia de la actuación"))
    user = ForeignKey(User, on_delete=CASCADE, help_text=_("Usuario que ha realizado la planificación de la actividad"))
    history = HistoricalRecordsLeadAction()

    class Meta:
        verbose_name = _("Actividad del lead")
        verbose_name_plural = _("Actividades del lead")

    @property
    def last_task(self):
        last_history_tasks = self.history_tasks.all().order_by('-id')
        for last_history_task in last_history_tasks.iterator():
            task = Task.objects.get(id=last_history_task.id)
            if not task.is_done:
                return last_history_task


class LeadCalendar(models.Model):
    lead = ForeignKey(Lead, help_text=_("Lead"), on_delete=DO_NOTHING)
    task = ForeignKey(Task, help_text=_("Tarea"), on_delete=DO_NOTHING)
    user = ForeignKey(User, help_text=_("Usuario"), on_delete=DO_NOTHING)
    status = CharField(max_length=255, help_text=_("Estado"))
    result = CharField(max_length=255, help_text=_("Resultado"))

    date = DateTimeField(help_text=_("Fecha"))
    type = CharField(max_length=255, help_text=_("Tipo de evento en calendario"))
    subtype = CharField(max_length=255, help_text=_("Tipo de tarea en calendario"))

    class Meta:
        # This is a view with leads and tasks.
        # View file: sql_views/migrations/create_calendar_view.sql
        managed = False
        db_table = "lead_calendar_view"


class LeadWhatsAppMessage(TimeStampedModel):
    """
    Store WhatsApp message sended to lead client
    """
    lead = ForeignKey(Lead, on_delete=CASCADE, help_text=_("Lead"), related_name='whatsappmessage')

    message = TextField()

    class Meta:
        verbose_name = _("Mensaje de WhatsApp")
        verbose_name_plural = _("Mensajes de WhatsApp")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        LeadManagement.objects.create(
            lead=self.lead,
            event=EVENT_OUTCOMING_WHATSAPP_KEY,
            message='WhatsApp enviado',
            status=self.lead.status,
            user=self.lead.user
        )
