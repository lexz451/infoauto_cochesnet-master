# -*- coding: utf-8 -*-

import datetime

import pytz
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from infoauto.leads.models.leads import LeadAction
from infoauto.leads.serializers.core import HistoricalTaskSerializer
from infoauto.leads.serializers.historical_leads import HisoricalLeadSerializer
from infoauto.leads_public.serializers import WritableNestedModelSerializer
from infoauto.users.serializers.users import SimplestUserSerializer


class BaseLeadActionSerializer(WritableNestedModelSerializer):
    user_data = SimplestUserSerializer(source='user', read_only=True)
    history_lead = HisoricalLeadSerializer(read_only=True)
    last_task = HistoricalTaskSerializer(read_only=True)

    class Meta:
        model = LeadAction
        editable_fields = ("lead", "lead_status_planing", "date")  # Only editable fields by API
        fields = (
            "id", 'history_lead', 'history_tasks', 'last_task', "user", 'user_data', 'status'
        ) + editable_fields
        read_only_fields = ('history_tasks', "user", 'user_data', 'status')
        extra_kwargs = {"date": {"required": False, 'allow_null': True}}

    def get_lead_history(self, validated_data):
        lead = validated_data['lead']
        lead_history = lead.history.all().order_by('history_id').last()
        if not lead_history:
            lead.save()
            validated_data['lead'] = lead
            lead_history = lead.history.all().order_by('history_id').last()
        return lead_history

    def validate(self, attrs):
        lead_action = attrs['lead'].leadaction_set.all().order_by('date', 'id').last()
        now = datetime.datetime.now().astimezone(pytz.UTC).replace(tzinfo=None)
        date = lead_action.date.astimezone(pytz.UTC).replace(tzinfo=None) if lead_action else None
        if not attrs.get('date') and date and (date > now):
            attrs['date'] = lead_action.date
        elif attrs.get('date'):
            if attrs['date'].astimezone(pytz.UTC).replace(tzinfo=None) < now:
                raise ValidationError({'date': _("La fecha tiene que ser igual o superior a la actual")})
            else:
                pass
        else:
            raise ValidationError({'date': _("Este campo es obligatorio")})
        return super().validate(attrs=attrs)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['history_lead'] = self.get_lead_history(validated_data)
        lead = validated_data['lead']
        history_tasks = [task.history.all().order_by('history_id').last()
                         for task in lead.request.task.all()
                         if task.history.all().order_by('history_id').last()]
        validated_data['history_tasks'] = history_tasks
        lead.status = validated_data['lead_status_planing']
        lead.save()
        validated_data['lead'] = lead
        return super().create(validated_data)


class LeadActionSerializer(BaseLeadActionSerializer):
    history_tasks = HistoricalTaskSerializer(read_only=True, many=True)
    client_name = CharField(source='lead.client.name', default=None, read_only=True)
    current_lead_status = CharField(source='lead.status', default=None, read_only=True)

    class Meta(BaseLeadActionSerializer.Meta):
        fields = BaseLeadActionSerializer.Meta.fields + ('client_name', 'current_lead_status')
        read_only_fields = BaseLeadActionSerializer.Meta.read_only_fields + ('client_name', 'current_lead_status')



