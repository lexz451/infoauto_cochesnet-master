# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import time

import requests

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from infoauto.leads.serializers.comment import CommentSerializer
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField, CharField, SerializerMethodField, BooleanField
from rest_framework.serializers import ModelSerializer

from infoauto.clients.serializers import ClientSerializer
from infoauto.common.util_email import send_email
from infoauto.concessionaires.serializers import ConcessionaireSerializer
from infoauto.leads.lead_master import LeadMaster
from infoauto.leads.models import Lead, UserConcession, ACD, LeadCalendar, LeadWhatsAppMessage
from infoauto.leads.models.lead_management import LeadManagement

from infoauto.leads.serializers.lead_actions import BaseLeadActionSerializer
from infoauto.leads.serializers.origins import OriginSerializer
from infoauto.leads.serializers.core import RequestSerializer, TaskSerializer, CommonTaskSerializer, AppraisalSerializer
from infoauto.leads.serializers.notes import NoteSerializer
from infoauto.leads.utils import get_concession_instance, enforce_timezone
from infoauto.source_channels.serializers import SourceSerializer, ChannelSerializer
from infoauto.users.serializers.users import SimplestUserSerializer
from infoauto.tags_app.serializers import TagSerializer
from infoauto.users.serializers import ComplexUserCreateSerializer
from infoauto.vehicles.serializers import VehicleSerializer
from datetime import timedelta
from django.conf import settings


GREEN = "#009688"
YELLOW = "#f39400"
BLUE = "#2196f3"
PURPLE = "#673ab7"
RED = "#f44336"
WHITE = "#ffffff"
BLACK = "#000000"

LEAD_STATUS_NEW = "new"
LEAD_STATUS_ATTENDED = "attended"
LEAD_STATUS_PENDING = "pending"
LEAD_STATUS_COMMERCIAL_MANAGEMENT = "commercial_management"
LEAD_STATUS_TRACING = "tracing"
LEAD_STATUS_END = "end"


class LeadCalendarSerializer(ModelSerializer):

    id = SerializerMethodField(read_only=True)
    title = SerializerMethodField(read_only=True)
    allDay = SerializerMethodField(read_only=True)
    color = SerializerMethodField(read_only=True)
    textColor = SerializerMethodField(read_only=True)
    resourceIds = SerializerMethodField(read_only=True)
    selectable = SerializerMethodField(read_only=True)
    description = SerializerMethodField(read_only=True)

    start = SerializerMethodField(read_only=True)
    end = SerializerMethodField(read_only=True)

    def get_id(self, lead_cal):
        return lead_cal.lead.pk

    def get_title(self, lead_cal):
        if lead_cal.lead and lead_cal.lead.client:
            return lead_cal.lead.client.get_full_name()
        return ""

    def get_start(self, lead_cal):
        return enforce_timezone(lead_cal.date)

    def get_end(self, lead_cal):
        return enforce_timezone(lead_cal.date + timedelta(minutes=15))

    def get_allDay(self, lead_cal):
        return False

    def get_color(self, lead_cal):
        color_mapping = {
            "pending_lead": GREEN,
            "pending_task": BLUE,
            "pending_traking": PURPLE,
        }
        return color_mapping[lead_cal.type]

    def get_textColor(self, lead_cal):
        if self.get_color(lead_cal) in [GREEN, BLUE]:
            return BLACK
        return WHITE

    def get_resourceIds(self, lead_cal):
        return lead_cal.lead.pk

    def get_selectable(self, lead_cal):
        return True

    def get_description(self, lead_cal):
        if lead_cal.type == "pending_lead":
            return "Lead no atendido"
        if lead_cal.type == "pending_task":
            return "Tarea programada: " + lead_cal.task.get_type_display()
        if lead_cal.type == "pending_traking":
            return "Seguimiento programado: " + lead_cal.task.get_type_display()

    class Meta:
        model = LeadCalendar
        fields = (
            'id',
            'title',
            'allDay',
            'color',
            'textColor',
            'resourceIds',
            'selectable',
            'description',
            'start',
            'end'
        )


class LeadManagementSerializer(ModelSerializer):
    user_data = SimplestUserSerializer(source='user', read_only=True)

    class Meta:
        model = LeadManagement
        fields = ['id', 'message', 'status', 'event', 'user_data', 'created']
        read_only_fields = fields


class LeadSimpleSerializer(WritableNestedModelSerializer):
    vehicles_names = SerializerMethodField()
    client_name = CharField(source='client.name', default=None)
    client_phone = CharField(source='client.phone', default=None)
    concession_id = CharField(source='concessionaire.id', default=None)
    concession_name = CharField(source='concessionaire.name', default=None)

    class Meta:
        model = Lead
        fields = ('id', 'user_id', 'vehicles_names', 'client_name', 'client_phone', 'concession_id', 'concession_name')
        read_only_fields = fields

    def get_vehicles_names(self, obj):
        v = []
        for vehicle in obj.vehicles.all():
            v.append(str(vehicle))
        return v


class LeadColumnSerializer(WritableNestedModelSerializer):
    vehicles_names = SerializerMethodField()
    client_name = CharField(read_only=True, source='client.name')
    client_surname = CharField(read_only=True, source='client.surname')
    client_business_name = CharField(read_only=True, source='client.business_name')
    client_phone = CharField(read_only=True, source='client.phone')
    channel = CharField(read_only=True)
    origin = SerializerMethodField(read_only=True)
    user_data = SimplestUserSerializer(source='user', read_only=True)
    last_lead_action = BaseLeadActionSerializer(read_only=True)
    last_task = SerializerMethodField(read_only=True)
    actions_number = SerializerMethodField()

    lead_managements_data = LeadManagementSerializer(many=True, source='lead_managements')

    class Meta:
        model = Lead
        fields = (
            'id',
            'score',
            'vehicles_names',
            'client_name',
            'client_surname',
            'client_business_name',
            'client_phone',
            'channel',
            'origin',
            'result',
            'result_reason',
            'user',
            'user_data',
            'last_lead_action',
            'actions_number',
            'last_task',
            'lead_managements_data'
        )

        read_only_fields = fields

    def get_last_task(self, obj):
        if obj.request:
            task = obj.request.task.filter(
                planified_realization_date__gte=datetime.datetime.now()
            ).order_by('planified_realization_date').first()

            return CommonTaskSerializer(task, many=False).data

    def get_vehicles_names(self, obj):
        v = []
        for vehicle in obj.vehicles.all():
            v.append(str(vehicle))
        return v

    def get_origin(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.origin.icon.url) if obj and obj.origin and obj.origin.icon and obj.origin.icon.url else None
        else:
            return None

    def get_actions_number(self, obj):
        return obj.leadaction_set.count()


class ACDSerializer(WritableNestedModelSerializer):
    concession = ConcessionaireSerializer(read_only=True)
    possible_leads = LeadColumnSerializer(many=True, read_only=True)

    class Meta:
        model = ACD
        fields = ('id', 'acd_remote_id', 'orig_phone', 'dest_phone', 'acd_audio', 'acd_audio_link',
                  'answered_call', 'date_contact', 'duration', 'lead', 'concession', 'possible_leads')

    def validate(self, attrs):
        if not self.instance and not get_concession_instance(phone=attrs['dest_phone']):
            raise ValidationError(_("El concesionario no existe"))
        return super().validate(attrs=attrs)


class WhatsAppSerializer(WritableNestedModelSerializer):

    class Meta:
        model = LeadWhatsAppMessage
        fields = ('id', 'lead', 'message', 'created')


class LeadSerializer(WritableNestedModelSerializer):
    client = ClientSerializer(allow_null=True, required=False)
    vehicles = VehicleSerializer(many=True, required=False)
    appraisals = AppraisalSerializer(many=True, required=False)
    request = RequestSerializer(required=False)
    user_data = ComplexUserCreateSerializer(read_only=True, source='user')
    pending_tasks = BooleanField(read_only=True)
    note = NoteSerializer(allow_null=True, many=True, required=False)
    comments = CommentSerializer(allow_null=True, many=True,read_only=True)
    first_task_date = DateTimeField(read_only=True)
    concessionaire_data = ConcessionaireSerializer(read_only=True, source='concessionaire', )
    nsa = CharField(read_only=True)
    origin = OriginSerializer(read_only=True)
    cur_user_can_assign = SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, allow_null=True, required=False)
    source_data = SourceSerializer(read_only=True, source='source')
    origin2_data = OriginSerializer(read_only=True, source='origin2')
    channel2_data = ChannelSerializer(read_only=True, source='channel2')
    status_dates = SerializerMethodField()
    last_lead_action = BaseLeadActionSerializer(read_only=True)
    last_lead_action_update = BaseLeadActionSerializer(read_only=True)
    current_user_is_concession_admin = SerializerMethodField()
    current_user_is_business_manager = SerializerMethodField()
    lead_managements = LeadManagementSerializer(many=True, read_only=True)

    class Meta:
        model = Lead
        fields = (
            'id',
            'concessionaire',
            'concessionaire_data',
            'client',
            'vehicles',
            'appraisals',
            'sent_whatsapp_count',
            'sent_phone_call_count',
            'sent_emails_count',
            'task_count',
            'tracking_count',
            'request',
            'request_type',
            'request_notes',
            'note',
            'comments',
            'end_date',
            'user',
            'user_data',
            'result',
            'result_reason',
            'result_comments',
            'created',
            'modified',
            'status',
            'score',
            'finish_date',
            'pending_tasks',
            'mail_content',
            'first_task_date',
            'nsa',
            'origin',
            'cur_user_can_assign',
            'tags',
            'source',
            'source2',
            'source_data',
            'origin2_data',
            'channel2_data',
            'origin2',
            'channel2',
            'status_dates',
            'psa_id',
            'last_lead_action',
            'last_lead_action_update',
            'current_user_is_concession_admin',
            'current_user_is_business_manager',
            'is_reactivated',
            'reactivated_date',
            'before_reactivated_finish_date',
            'before_reactivated_result',
            # status datetimes
            'status_new_datetime',
            'status_pending_datetime',
            'status_attended_datetime',
            'status_tracing_datetime',
            'status_end_datetime',
            # custom status dates.
            'custom_status_new_datetime',
            'custom_status_pending_datetime',
            'custom_status_attended_datetime',
            'custom_status_tracing_datetime',
            'custom_status_end_datetime',
            'lead_managements',
        )

        extra_kwargs = {
            'user': {'required': False},
            'created': {'read_only': True},
            'status': {'required': False},
            'finish_date': {'read_only': True},
            'concessionaire_data': {'read_only': True},
            'concessionaire': {'required': True},
            'source': {'required': True},
            'score': {'required': True, "error_messages": {"required": "Es obligatorio, valorar el lead."}},
            'is_reactivated': {'read_only': True},
            'reactivated_date': {'read_only': True},
            'before_reactivated_finish_date': {'read_only': True},
            'before_reactivated_result': {'read_only': True},
            'attended_date': {'read_only': True},
            'status_new_datetime': {'read_only': True},
            'status_pending_datetime': {'read_only': True},
            'status_attended_datetime': {'read_only': True},
            'status_tracing_datetime': {'read_only': True},
            'status_end_datetime': {'read_only': True},
            'custom_status_new_datetime': {'write_only': True},
            'custom_status_pending_datetime': {'write_only': True},
            'custom_status_attended_datetime': {'write_only': True},
            'custom_status_tracing_datetime': {'write_only': True},
            'custom_status_end_datetime': {'write_only': True}
        }

    def get_status_dates(self, obj):
        data = {}
        if not obj.is_reactivated:
            for i in obj.history.all().order_by('history_id').values('status', 'history_date'):
                data[i['status']] = i['history_date']
        else:
            for i in obj.history.filter(modified__gte=obj.reactivated_date).order_by('history_id').values('status', 'history_date'):
                data[i['status']] = i['history_date']
        return data

    def is_valid(self, raise_exception=False):
        if self.initial_data.get('client'):
            check_client = [i for i in self.initial_data['client'].values() if i]
            if not check_client:
                self.initial_data.pop('client', None)
        return super().is_valid(raise_exception)

    def validate(self, attrs):
        if self.instance and attrs.get("user") and attrs["user"] != self.instance.user:
            if not self.get_cur_user_can_assign(self.instance):
                raise ValidationError({"user": _("No tiene permisos para realizar esta acción")})
            if self.instance.concessionaire.id not in attrs['user'].userconcession_set.all().values_list('concessionaire', flat=True):
                raise ValidationError({'user': _("El usuario no pertenece al concesionario asignado al lead")})
        if not self.instance and attrs.get('request', None) is None:
            attrs['request'] = {}
            self.initial_data.update({'request': {}})

        if attrs.get("result") == 'negative' and attrs.get("result_reason") == 'otro':
            if not attrs.get("result_comments"):
                raise ValidationError({'result_comments': _("Debe indicar el motivo.")})

        status = attrs.get('status', self.instance.status if self.instance else None)
        if status == 'end':
            if self.instance.tasks.filter(realization_date_check=False).exists():
                raise ValidationError({'non_field_errors': [_("Debe finalizar las tareas y seguimientos.")]})
            error = {'client': {}, 'vehicles': [{}], 'non_field_errors': [
                _("Debe completar datos del lead antes de cerrarlo")]}
            has_error = False

            win = attrs.get('result', self.instance.result)
            if win == 'positive':
                if (not self.instance or not self.instance.client or not self.instance.client.name) and (not 'client' in attrs or not 'name' in attrs.get('client') or not attrs.get('client').get('name')):
                    error['client']['name'] = [_("Debe completar este campo.")]
                    has_error = True
                if (not self.instance or not self.instance.client or not self.instance.client.surname) and (not 'client' in attrs or not 'surname' in attrs.get('client') or not attrs.get('client').get('surname')):
                    error['client']['surname'] = [_("Debe completar este campo.")]
                    has_error = True
                if (not self.instance or not self.instance.client or not self.instance.client.email) and (not 'client' in attrs or not 'email' in attrs.get('client') or not attrs.get('client').get('email')):
                    error['client']['email'] = [_("Debe completar este campo.")]
                    has_error = True
            if (not self.instance or not self.instance.client or not self.instance.client.phone) and (not 'client' in attrs or not 'phone' in attrs.get('client') or not attrs.get('client').get('phone')):
                error['client']['phone'] = [_("Debe completar este campo.")]
                has_error = True
            if (not self.instance.vehicles.exists() or not self.instance.vehicles.first().brand_model) and (not 'vehicles' in attrs or not 'brand_model' in attrs.get('vehicles')[0]):
                error['vehicles'][0]['brand_model'] = [_("Debe completar este campo.")]
                has_error = True
            if (not self.instance.vehicles.exists() or not self.instance.vehicles.first().model) and (not 'vehicles' in attrs or not 'model' in attrs.get('vehicles')[0]):
                error['vehicles'][0]['model'] = [_("Debe completar este campo.")]
                has_error = True
            if (not self.instance.vehicles.exists() or not self.instance.vehicles.first().vehicle_type) and (not 'vehicles' in attrs or not 'vehicle_type' in attrs.get('vehicles')[0]):
                error['vehicles'][0]['vehicle_type'] = [_("Debe completar este campo.")]
                has_error = True
            if has_error:
                raise ValidationError(error)

        else:
            presential = attrs.get('channel2', self.instance.channel2 if self.instance else None)
            print(presential)
            if presential:
                error = {'client': {}, 'non_field_errors': [_("Debe completar datos del lead antes de cerrarlo")]}
                has_error = False

                if (not self.instance or not self.instance.client or not self.instance.client.name) and (not 'client' in attrs or not 'name' in attrs.get('client') or not attrs.get('client').get('name')):
                    error['client']['name'] = [_("Debe completar este campo.")]
                    has_error = True
                if (not self.instance or not self.instance.client or not self.instance.client.surname) and (not 'client' in attrs or not 'surname' in attrs.get('client') or not attrs.get('client').get('surname')):
                    error['client']['surname'] = [_("Debe completar este campo.")]
                    has_error = True
                if (not self.instance or not self.instance.client or not self.instance.client.email) and (not 'client' in attrs or not 'email' in attrs.get('client') or not attrs.get('client').get('email')):
                    error['client']['email'] = [_("Debe completar este campo.")]
                    has_error = True
                if (not self.instance or not self.instance.client or not self.instance.client.phone) and (not 'client' in attrs or not 'phone' in attrs.get('client') or not attrs.get('client').get('phone')):
                    error['client']['phone'] = [_("Debe completar este campo.")]
                    has_error = True

                if has_error:
                    raise ValidationError(error)

        return super().validate(attrs)

    def create(self, validated_data):
        if not validated_data.get('user'):
            validated_data['user'] = self.context['request'].user
        validated_data['concessionaire'] = validated_data['source'].concession
        instance = super().create(validated_data)
        self.instance = instance
        self.send_user_notification()
        c_id = self.instance.concessionaire.id
        c_ids = [1, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 68, 79, 81, 83, 99, 123]
        if (c_id in c_ids):
            print('-------------------------------------------------')
            print(f'Sending PN request for concessionaire id: {c_id}')
            self.sendPN()
        # return self.post_create(instance)
        self.checkWATIEligible()
        return instance

    def update(self, instance, validated_data):
        old_user = self.instance.user
        instance = super().update(instance, validated_data)
        self.send_user_notification(old_user=old_user)
        # self.sendPN(data=self.instance)
        # self.checkWATIEligible()
        return instance

    def checkWATIEligible(self):
        self.sendWSTemplate()
        return

    def sendWSTemplate(self):
        #
        wati_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5MTY2MzQ3NS0xMmZmLTQwZjEtYTZmNy0wOTk3OWZmYTFmOTkiLCJ1bmlxdWVfbmFtZSI6InNjbGVtZW50ZUBpbmZvLWF1dG8uZXMiLCJuYW1laWQiOiJzY2xlbWVudGVAaW5mby1hdXRvLmVzIiwiZW1haWwiOiJzY2xlbWVudGVAaW5mby1hdXRvLmVzIiwiYXV0aF90aW1lIjoiMDQvMjEvMjAyMiAwNTozNDoxMSIsImRiX25hbWUiOiI3MzI1IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQURNSU5JU1RSQVRPUiIsImV4cCI6MjUzNDAyMzAwODAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.5wj6dBMcOabSz-UmjhMdbkXE3qRGpKN16DoOMfdB1m4'
        wati_url = 'https://live-server-7325.wati.io'

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {wati_token}"
        }

        client_phone = self.instance.client.phone
        client_name = self.instance.client.name
        client_id = self.instance.client.id
        lead_id = self.instance.id

        client_phone = client_phone.replace('+', '')

        addContact = {
            "name": client_name,
            "customParams": [
                {
                    "name": "lead_id",
                    "value": lead_id
                },
                {
                    "name": "client_id",
                    "value": client_id
                }
            ]
        }

        addContactData = json.dumps(addContact)

        addContactUrl = f"{wati_url}/api/v1/addContact/{client_phone}"
        
        resContact = requests.post(url=addContactUrl, data=addContactData, headers=headers)
        if (resContact.ok):
            print("WATI contact created!. Continue...")
            print(resContact.text)
        else:
            print("Error creating WATI contact (halting execution!):")
            print(resContact.text)
            return    

        sendTemplateUrl = f"{wati_url}/api/v1/sendTemplateMessage?whatsappNumber={client_phone}"
        sendTemplate = {
            "template_name": "posventa_llamadasperdidas",
            "broadcast_name": f"posventa_llamadasperdidas_lead_{client_phone}",
            "parameters": [
                {
                    "name": "lead_id",
                    "value": lead_id
                },
                {
                    "name": "client_id",
                    "value": client_id
                }
            ]
        }

        sendTemplateData = json.dumps(sendTemplate)

        res = requests.post(url=sendTemplateUrl, data=sendTemplateData, headers=headers)
        if (res.ok):
            print("WATI Template sent!")
            print(res.text)
        else:
            print(f"Error sending WATI template:")
            print(res.text)
        return

    def sendPN(self):
        appKey = 'SAILS'
        consumerKey = '1r9qsfhwmkywvyllxexuw5j54'
        consumerSecret = "CO12345CO"
        url = 'https://drivim.vozipcenter.com/api/nuevo_contacto'
        method = 'POST'

        client_name = self.instance.client.name
        client_phone = self.instance.client.phone
        lead_id = self.instance.id
        
        local_time = time.time()
        server_time = int(requests.get('https://drivim.vozipcenter.com/api/time').text)
        diff = server_time - local_time

        data = {
            "modificable": True,
            "grupo": "MARCADOR",
            "nombre": client_name,
            "numero": client_phone,
            "bd": "BBDD",
            "campos": {
                "ID": f"https://sail.artificialintelligencelead.com/leads/{lead_id}/edit"
            }
        }

        print(f'PN payload: {data}')

        payload = json.dumps(data).replace(" ", "")

        timestamp = str(time.time() + diff)

        sha1_payload = f"{consumerSecret}+{consumerKey}+{method}+{url}+{payload}+{timestamp}".encode('utf-8')

        sha1 = hashlib.sha1(sha1_payload).hexdigest()

        signature = "$1$" + sha1

        headers = {
            "Content-Type": "application/json",
            "CC-Application": appKey,
            "CC-Timestamp": timestamp,
            "CC-Signature": signature,
            "CC-Consumer": consumerKey
        }

        req = requests.post(url=url, data=payload, headers=headers)
        print(f'PN response: {req.text}')
        print('-------------------------------------------------')

    def send_user_notification(self, old_user=None):
        if (not old_user or (self.instance.user != old_user)) and self.context.get("request") and self.instance.user:
            request = self.context['request']
            lead_url = "{0}/leads/{1}/edit".format(request._current_scheme_host, self.instance.id)
            call_url = "{0}/leads/{1}/call".format(request._current_scheme_host, self.instance.id)

            context = {
                'lead': self.instance,
                'lead_url': lead_url,
                'call_url': call_url,
                'domain_url': request._current_scheme_host
            }

            try:
                send_email(to_email=[self.instance.user.email],
                           subject=_('Alerta de alta de lead'),
                           template='email/new_lead', context=context, request=self.context['request'],
                           smtp_config_name="lead_user_assign")
            except Exception as e:
                print(e)
                print(settings.SMTP_CONFIG)

    def delete_reverse_relations_if_need(self, instance, reverse_relations):
        pass

    def get_cur_user_can_assign(self, obj):
        """
        Return True or False if current user has permissions to assign leads. (business_manager can't assign leads)
        :param obj: Lead instance
        :return: Boolean (True|False)
        """
        is_concession_admin = self.get_current_user_is_concession_admin(obj)
        is_business_manager = self.get_current_user_is_business_manager(obj)
        if not self.context['request'].user.is_admin and not is_concession_admin and is_business_manager:
            return False
        return True

    def get_current_user_is_concession_admin(self, obj):
        return UserConcession.objects.filter(
            concessionaire=obj.concessionaire, user=self.context['request'].user,
            is_concessionaire_admin=True).exists()

    def get_current_user_is_business_manager(self, obj):
        return UserConcession.objects.filter(
            concessionaire=obj.concessionaire, user=self.context['request'].user,
            is_business_manager=True).exists()

    def to_representation(self, instance):
        view = self.context.get("view")
        if view and view.action not in ['retrieve']:
            self.fields.pop('history', None)
        getattr(self.fields.get('user_data', None), 'fields', {}).pop('related_concessionaires', None)
        try:
            self.fields['request'].fields['task'].child.fields['author_data'].fields.pop('related_concessionaires')
        except:
            pass
        try:
            self.fields['request'].fields['task'].child.fields['author_data'].fields.pop('session')
        except:
            pass
        try:
            self.fields['concessionaire_data'].fields['sources'].child.fields['origin_data'].fields.pop(
                'available_channels')
        except:
            pass
        try:
            self.fields['concessionaire_data'].fields['sources'].child.fields['origin_data'].fields.pop(
                'available_channels_data')
        except:
            pass
        return super().to_representation(instance)


class ExcelLeadSerializer(WritableNestedModelSerializer):
    nameconcession = CharField(source='concessionaire.name', default=None)
    historic = SerializerMethodField(read_only=True)
    client_name = CharField(source='client.name', default=None)
    client_phone = CharField(source='client.phone', default=None)
    """
    vehicle_brand_model = CharField(source='vehicle.brand_model')
    vehicle_price = CharField(source='vehicle.price')
    vehicle_km = CharField(source='vehicle.km')
    vehicle_year = CharField(source='vehicle.year')
    vehicle_gas = CharField(source='vehicle.gas.name', default=None)
    """
    owned_by = CharField(source='user.username', default=None)
    notes = SerializerMethodField(read_only=True)
    nsa_years = SerializerMethodField(read_only=True)
    nsa_months = SerializerMethodField(read_only=True)
    nsa_days = SerializerMethodField(read_only=True)
    nsa_hours = SerializerMethodField(read_only=True)
    nsa_minutes = SerializerMethodField(read_only=True)
    nsa_seconds = SerializerMethodField(read_only=True)
    last_realization_task = CharField(read_only=True)
    last_tracking_task = CharField(read_only=True)
    origin = CharField(source="origin.name", default=None)
    medio = CharField(source='source.channel.name', default=None)
    province = CharField(source='client.province.name', default=None)
    score = CharField(source="get_score_display")
    cita = SerializerMethodField()
    tasacion = SerializerMethodField()
    presupuesto = SerializerMethodField()
    financiacion = SerializerMethodField()
    garantia = SerializerMethodField()
    info_vehiculo = SerializerMethodField()
    respuesta_mail = SerializerMethodField()
    otros = SerializerMethodField()
    Canal = CharField(source="source.channel.name", default=None)
    Fuente = CharField(source="source.data", default=None)

    class Meta:
        model = Lead
        fields = ("id", "nameconcession", "Canal", "Fuente", "origin", "medio", "status", "client_name",
                  "client_phone", "province",
                  # "vehicle_brand_model", "vehicle_price", "vehicle_km", "vehicle_year", 'vehicle_gas',
                  'notes', "owned_by", "score", "result", "historic", "created",
                  "nsa_years", "nsa_months", "nsa_days", "nsa_hours", "nsa_minutes", "nsa_seconds",
                  "last_realization_task", "last_tracking_task", "cita", "tasacion", "presupuesto", "financiacion",
                  "garantia", "info_vehiculo", "respuesta_mail", "otros")
        read_only_fields = fields

    def get_notes(self, obj):
        return '\n\n'.join(obj.note.all().values_list('content', flat=True)) if obj.note.all() else None

    def get_historic(self, obj):
        data = ["Usuario: %(user)s; Fecha: %(date)s; Duración: %(duration)s" % {
            'user': getattr(obj.user, 'username', ""), 'date': i.date_contact, 'duration': i.duration}
            for i in obj.acd_set.all()]
        return "\n\n".join(data) if data else None

    def get_cita(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='date') else 0

    def get_tasacion(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='appraisal') else 0

    def get_presupuesto(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='budget') else 0

    def get_financiacion(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='financing') else 0

    def get_garantia(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='warranty') else 0

    def get_info_vehiculo(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='info_vehiculo') else 0

    def get_respuesta_mail(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='response_information_mail') else 0

    def get_pendinete_asignacion(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='pending_assignment') else 0

    def get_otros(self, obj):
        return 1 if obj.request and obj.request.task.filter(type='other') else 0

    def get_nsa_years(self, obj):
        return obj.nsa['years'] if obj.nsa else None

    def get_nsa_months(self, obj):
        return obj.nsa['months'] if obj.nsa else None

    def get_nsa_days(self, obj):
        return obj.nsa['days'] if obj.nsa else None

    def get_nsa_hours(self, obj):
        return obj.nsa['hours'] if obj.nsa else None

    def get_nsa_minutes(self, obj):
        return obj.nsa['minutes'] if obj.nsa else None

    def get_nsa_seconds(self, obj):
        return obj.nsa['seconds'] if obj.nsa else None


class LeadStatusSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'status')
        extra_kwargs = {'status': {'required': True}}

    def validate(self, attrs):
        status = attrs['status']
        if status in ['end']:
            raise ValidationError({'status': _('Cambio de estado no permitido')})
        if self.instance and self.instance.status == 'end':
            attrs['result'] = None
        return super().validate(attrs)

    def update(self, instance, validated_data):
        setattr(self.instance, 'force_status', True)
        return super().update(instance, validated_data)


class LeadMasterSerializer(serializers.Serializer):
    class Meta:
        model = LeadMaster
        fields = '__all__'
