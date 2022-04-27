import datetime
from datetime import timedelta

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import EmailField, CharField, DateTimeField, OneToOneField, CASCADE, BooleanField, \
    SmallIntegerField, ForeignKey, PROTECT, TextField, Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
from rest_framework.authtoken.models import Token


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

USER_UNAVAILABLE_CHOICES = [
    ("asisting_clients", _('Atendiendo clientes')),
    ("breakfast", _('Desayunando')),
    ("bathroom", _('En el aseo')),
    ("excused", _('Ausencia justificada')),
]

class UserHistoricalRecords(HistoricalRecords):
    pass


class User(AbstractUser, TimeStampedModel):
    email = EmailField(_('email address'), blank=True, unique=True)
    phone = CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True,
        help_text=_("Numero de teléfono desde el que se ha llamado")
    )
    ubunet_extension = CharField(
        max_length=17, blank=True, null=True, default=None,
        help_text=_("Extension en Ubunet")
    )
    ubunet_company = CharField(
        max_length=17, blank=True, null=True, default=None,
        help_text=_("Company en Ubunet")
    )
    ubunet_agent = CharField(
        max_length=17, blank=True, null=True, default=None,
        help_text=_("Agente en Ubunet"), unique=True
    )
    user_activation_date = DateTimeField(blank=True, null=True)
    user_deactivation_date = DateTimeField(blank=True, null=True)
    last_action_date = DateTimeField(blank=True, null=True)
    memberid = CharField(max_length=255, blank=True, null=True, help_text=_("Member Id for Click2Call"))
    id_click2call = CharField(max_length=255, blank=True, null=True, help_text=_("Id for Click2Call"))
    is_available = BooleanField(
        default=False, help_text=_("Campo donde el usuario indica si se encuentra disponible o no para trabajar")
    )
    unavailable_reason = CharField(max_length=512, blank=True, choices=USER_UNAVAILABLE_CHOICES, help_text=_("Motivo trabajador no se encuentra disponible"))

    lost_calls = BooleanField(default=False, help_text=_("Llamadas perdidas"))
    emails_received = BooleanField(default=False, help_text=_("Email recibidos"))
    ddi_whatsapp_business = CharField(max_length=255, blank=True, null=True, help_text=_("DDis WhatsApp Business"))
    historical = UserHistoricalRecords()

    class Meta:
        ordering = ['first_name']

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def is_admin(self):
        if self.is_superuser or self.is_staff:
            return True
        else:
            return False

    @property
    def is_concession_admin(self):
        if self.userconcession_set.filter(is_concessionaire_admin=True).exists():
            return True
        else:
            return False

    def is_business_manager(self):
        if self.userconcession_set.filter(is_business_manager=True).exists():
            return True
        else:
            return False

    @property
    def current_authenticated(self):
        try:
            self.auth_token
            return True
        except Exception:
            return False

    @property
    def user_is_logged(self):
        return Token.objects.filter(user=self).first()

    @property
    def is_online(self):
        now = timezone.now()
        if self.last_action_date and (now - self.last_action_date).seconds <= settings.USER_ONLINE_TIMEOUT and self.user_is_logged:
            return True
        return False

    @property
    def today_lead_number(self):
        now = datetime.datetime.now()
        datetime.datetime.combine(now, datetime.time.min)
        date_range = (datetime.datetime.combine(now, datetime.time.min),
                      datetime.datetime.combine(now, datetime.time.max))
        return self.lead_set.filter(assigned_date__range=date_range).distinct().count()

    @property
    def last_lead_datetime(self):
        last_lead = self.lead_set.all().order_by('-assigned_date').first()
        if last_lead:
            return last_lead.assigned_date

    @property
    def unattended_leads(self):
        return self.lead_set.filter(status='new').count()

    @property
    def delayed_tasks(self):
        from infoauto.leads.models import Task

        return Task.objects.filter(
            lead__in=self.lead_set.all(),
            realization_date_check=False,
            planified_realization_date__lt=timezone.now(),
            is_traking_task=False
        ).count()

    @property
    def delayed_trackings(self):
        from infoauto.leads.models import Task
        return Task.objects.filter(
            lead__in=self.lead_set.all(),
            realization_date_check=False,
            realization_date__lt=timezone.now(),
            is_traking_task=True
        ).count()


CHANNEL_EMAIL_KEY = "email"
CHANNEL_SMS_KEY = "sms"

CHANNELS_OPTS = [
    (CHANNEL_EMAIL_KEY, _('Email')),
    (CHANNEL_SMS_KEY, _('SMS')),
]

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


EVENTS_OPTS = [
    (EVENT_LEAD_NOT_ATTENDED_KEY, _('Lead no atendido')),
    (EVENT_LEAD_ATTENDED_KEY, _('Lead atendido')),
    (EVENT_LEAD_END_KEY, _('Lead finalizado')),
    (EVENT_LEAD_CREATE_TASK_KEY, _('Nueva tarea creada en lead')),
    (EVENT_LEAD_DONE_TASK_KEY, _('Tarea finalizada en lead')),
    (EVENT_LEAD_CREATE_TRAKING_KEY, _('Nuevo seguimiento en lead')),
    (EVENT_LEAD_DONE_TRAKING_KEY, _('Seguimiento finalizado en lead')),
    (EVENT_INCOMING_CALL_KEY, _('Llamada entrante en lead')),
    (EVENT_OUTCOMING_CALL_KEY, _('Llamada saliente en lead')),
]

class UserSFA(TimeStampedModel):
    user = ForeignKey(User, on_delete=PROTECT, related_name="sfa_configurations")
    channel = CharField(max_length=224, choices=CHANNELS_OPTS, blank=False, null=False)
    event = CharField(max_length=224, choices=EVENTS_OPTS, blank=False, null=False)
    text = TextField()
    
class UserWhatsappTemplate(TimeStampedModel):
    user = ForeignKey(User, on_delete=PROTECT, related_name="whatsapp_templates")
    alias = CharField(max_length=224, blank=False, null=False, default='Plantilla sin nombre')
    text = TextField()


class SessionHistoricalRecords(HistoricalRecords):

    def post_save(self, instance, created, **kwargs):
        """
        Customized post_save - Do not save historic when created instance
        :param instance: SessionWithHistoric instance
        :param created: Instance is created (True | False)
        :param kwargs: Extra parameters
        :return: None
        """
        if created or (not created and hasattr(instance, 'skip_history_when_saving')):
            return
        if not kwargs.get('raw', False):
            self.create_historical_record(instance, created and '+' or '~')


class SessionWithHistoric(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE)
    start_working = DateTimeField(blank=True, null=True, help_text=_("User starts to work"))
    last_seen = DateTimeField(blank=True, null=True, )
    end_working = DateTimeField(blank=True, null=True, help_text=_("Last time when user was working"))
    forced_online_status = BooleanField(default=True, help_text=_("If True, is currently working"))
    worked_hours = SmallIntegerField(blank=True, null=True)

    history = SessionHistoricalRecords()

    class Meta:
        verbose_name = _("Session With Historic")
        verbose_name_plural = _("Sessions With Historic")

    def check_last_seen(self):
        last_seen = self.last_seen
        if last_seen:
            valid_datetime = self.last_seen + timedelta(seconds=settings.USER_ONLINE_TIMEOUT)
            if (valid_datetime >= timezone.now()) and self.user.current_authenticated:
                # It hast to return True but depends of forced_online_status (True or False)
                return self.forced_online_status
            else:
                self.end_working = last_seen
                self.last_seen = None
                self.save()
                # This result always be False. Not depend of forced_online_status
        return False

    @property
    def online(self):
        return self.check_last_seen()

    def calc_active_time_yesterday(self):
        yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
        yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min).replace(tzinfo=pytz.utc)
        yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max).replace(tzinfo=pytz.utc)
        values = self.history.filter(
            start_working__range=(yesterday_min, yesterday_max)
        ).values_list("end_working", "start_working")
        hours = sum([(i[0] - i[1]).days * 24 + (i[0] - i[1]).seconds / 3600 for i in values])
        self.worked_hours = round(hours)
        setattr(self, 'skip_history_when_saving', True)
        self.save()
        return hours

    @property
    def active_time_yesterday(self):
        return self.calc_active_time_yesterday()

    def __str__(self):
        return "Historic Id: %d - User: %s" % (self.id, self.user.username)
