import datetime
from collections import OrderedDict

import pytz
from django.apps import apps

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from infoauto.users.serializers import ComplexUserCreateSerializer
from infoauto.leads.models import Request, Appraisal, Task, Lead
from infoauto.vehicles.serializers import GasTypeSerializer


class AppraisalSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Appraisal
        fields = (
            'id',
            'lead',
            'brand',
            'model',
            'version',
            'km',
            'status',
            'features',
            'circulation_date',
            'evaluation_vo_price',
            'total_vehicles',
            'total_comercial_vehicles',
            'total_tourism_vehicles',
            'fleet_notes',
            'license_plate',
            'buy_date',
            'registration_date',
            'last_mechanic_date',
            'cv',
            'is_finance'
        )


class CommonTaskSerializer(WritableNestedModelSerializer):
    appraisal = AppraisalSerializer(required=False, allow_null=True)
    # note = NoteSerializer(allow_null=True, many=True, required=False)

    class Meta:
        model = Task
        fields = (
            'id', 'type', 'subtype', 'description', 'media',
            'planified_realization_date', 'planified_tracking_date', 'realization_date',
            'realization_date_check', 'tracking_date', 'tracking_date_check', 'created', 'appraisal',
            'is_click2call', 'author', 'is_traking_task'
        )
        extra_kwargs = {
            'created': {'read_only': True},
            'request_data': {'required': False, "read_only": True},
            #'realization_date': {'read_only': True},
            'tracking_date': {'read_only': True},
            'subtype': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_null': True},
            'is_click2call': {'read_only': True},
            'author': {'required': False}
        }

    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        """
        Validation
        :param attrs: Parsed serializer data
        :return:
        """
        if attrs.get("planified_tracking_date"):
            if (attrs.get("planified_realization_date") and
                    attrs['planified_tracking_date'] < attrs.get("planified_realization_date")):
                raise ValidationError({
                    "planified_tracking_date": _("La fecha de seguimiento no puede ser menor a la fecha de realización")
                })
            elif (not attrs.get("planified_realization_date") and
                  attrs['planified_tracking_date'] < (
                      datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)) - datetime.timedelta(minutes=3))):
                raise ValidationError({
                    "planified_tracking_date": _("La fecha de seguimiento no puede ser menor al momento actual ya que no"
                                                "se ha planificado una fecha de realización")
                })
            elif (self.instance and self.instance.planified_realization_date and
                  not attrs.get("planified_realization_date") and
                  attrs.get("planified_tracking_date") < self.instance.planified_realization_date):
                raise ValidationError({
                    "planified_tracking_date": _("La fecha de seguimiento no puede ser menor a la fecha de realización")
                })
        return super().validate(attrs=attrs)

    def create(self, validated_data):
        """
        if 'realization_date' in validated_data.keys() and not validated_data['realization_date']:
            validated_data['realization_date'] = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        """
        if 'planified_realization_date' in validated_data.keys() and not validated_data['planified_realization_date']:
            validated_data['planified_realization_date'] = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        if validated_data.get("realization_date_check"):
            validated_data['realization_date'] = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        if validated_data.get("tracking_date_check"):
            validated_data['tracking_date'] = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        if 'realization_date' in validated_data.keys() and not validated_data['realization_date']:
            if not instance.realization_date:
                validated_data['realization_date'] = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
            else:
                validated_data.pop('realization_date', None)
        """
        if 'planified_realization_date' in validated_data.keys() and not validated_data['planified_realization_date']:
            if not instance.planified_realization_date:
                date_now = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
                validated_data['planified_realization_date'] = date_now
            else:
                validated_data.pop('planified_realization_date', None)
        if not self.instance.realization_date_check and validated_data.get("realization_date_check"):
            validated_data['realization_date'] = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        elif self.instance.realization_date_check and validated_data.get("realization_date_check") is False:
            validated_data['realization_date'] = None
        if not self.instance.tracking_date_check and validated_data.get("tracking_date_check"):
            validated_data['tracking_date'] = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        elif self.instance.tracking_date_check and validated_data.get("tracking_date_check") is False:
            validated_data['tracking_date'] = None
        return super().update(instance, validated_data)


class HistoricalTaskSerializer(WritableNestedModelSerializer):
    class Meta:
        model = apps.get_model('leads', model_name="HistoricalTask")
        fields = ['id', 'created', 'modified', 'type', 'subtype', 'description', 'media', 'realization_date',
                  'tracking_date', 'realization_date_check', 'tracking_date_check', 'planified_realization_date',
                  'planified_tracking_date', 'is_click2call', 'author', 'appraisal', 'history_id',
                  'history_change_reason', 'history_date', 'history_user', 'history_type']


class TaskSerializer(CommonTaskSerializer):
    author_data = ComplexUserCreateSerializer(read_only=True, source="author")
    # history = HistoricalTaskSerializer(read_only=True, many=True)

    class Meta(CommonTaskSerializer.Meta):
        new_fields = ('author_data', )
        fields = CommonTaskSerializer.Meta.fields + new_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            self.fields['author_data'].fields.pop('concessionaires', None)

    def validate(self, attrs):
        if not self.instance:
            attrs.update({'author': self.context['request'].user})
        """   
        if (attrs.get('tracking_date_check') and not attrs.get('tracking_date') and not
                (self.instance and not self.instance.tracing_date)):
            raise ValidationError(_("Tracing check can not be established where there is no tracing date."))
        """
        return super().validate(attrs)

    def to_representation(self, instance):
        view = self.context.get('view')
        if view and view.action not in ['retrieve']:
            self.fields.pop("history", None)
        return super().to_representation(instance)


class HistoricalRequestSerializer(WritableNestedModelSerializer):
    class Meta:
        model = apps.get_model('leads', model_name='HistoricalRequest')
        fields = ['id', 'created', 'modified', 'history_id', 'history_change_reason', 'history_date',
                  'history_user', 'history_type']


class RequestSerializer(WritableNestedModelSerializer):
    task = TaskSerializer(many=True, required=False)
    # history = HistoricalRequestSerializer(read_only=True, many=True)

    class Meta:
        model = Request
        fields = ('id', 'task')

    def to_representation(self, instance):
        view = self.context.get('view')
        if view and view.action not in ['retrieve']:
            self.fields.pop("history", None)
        return super().to_representation(instance)



class TaskCreateSerializer(CommonTaskSerializer):
    request = PrimaryKeyRelatedField(source='request_set', queryset=Request.objects.all(), many=True, required=False)
    request_data = RequestSerializer(read_only=True, many=True)

    class Meta(CommonTaskSerializer.Meta):
        new_fields = ('request', 'request_data', 'lead')
        fields = CommonTaskSerializer.Meta.fields + new_fields

    def validate(self, attrs):
        if not self.instance:
            attrs.update({'author': self.context['request'].user})
        return super().validate(attrs)


class LeadTaskCreateSerializer(CommonTaskSerializer):

    class Meta(CommonTaskSerializer.Meta):
        subclass_fields = ('lead', )
        fields = CommonTaskSerializer.Meta.fields + subclass_fields

    def validate(self, attrs):
        if not self.instance:
            attrs.update({'author': self.context['request'].user})
        return super().validate(attrs)

    def create(self, validated_data):
        #lead = validated_data.pop('lead')
        if not validated_data.get('planified_realization_date'):
            validated_data['planified_realization_date'] = None
        task = super().create(validated_data)
        lead.request.task.add(task)
        lead.request.save()
        return task


class TaskSimpleSerializer(WritableNestedModelSerializer):
    # date_literal = CharField(read_only=True)
    date_literal = serializers.ListField(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "type", "date_literal")


class RequestSimpleSerializer(WritableNestedModelSerializer):
    task = TaskSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'task')
