# coding: utf-8
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from infoauto.click2call.clients import Client
from infoauto.leads.models import Task, Lead


class Click2CallSerializer(WritableNestedModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all(), required=True, write_only=True)

    class Meta:
        model = Task
        fields = ('id', 'lead')

    def _check_client_phone(self):
        if not self.lead_instance.client or not self.lead_instance.client.phone:
            raise ValidationError(_("El cliente no tiene un teléfono asignado"))

    def _check_user_phone(self):
        if not self.user.phone:
            raise ValidationError(_("El usuario no tiene un teléfono asignado"))

    def _get_c2c_from_lead(self):
        if self.lead_instance:
            return self.lead_instance.request.task.filter(is_click2call=True).exists()
        return None

    def _set_realization_or_traking(self, data):
        c2c_exists = self._get_c2c_from_lead()
        if not c2c_exists and self.lead_instance.status in ['new', 'pending', 'commercial_management']:
            data.update({'realization_date': timezone.now(), 'realization_date_check': True})
        else:
            data.update({'tracking_date': timezone.now(), 'tracking_date_check': True})

    def _set_lead_status(self, task_instance):
        c2c_exists = self._get_c2c_from_lead()
        self.lead_instance.request.task.add(task_instance)
        if self.lead_instance.status in ['new', 'pending', 'commercial_management']:
            setattr(self.lead_instance, 'force_status', True)
            if not c2c_exists:
                self.lead_instance.status = 'commercial_management'
            else:
                self.lead_instance.status = 'tracing'
            self.lead_instance.save()

    def validate(self, attrs):
        self.lead_instance = attrs['lead']
        self.user = self.context['request'].user
        attrs.pop('lead')
        self._check_client_phone()
        self._check_user_phone()
        description = "El usuario %s (Tlf: %s) ha realizado una llamada a %s (Tlf: %s)" % (
            self.user.get_full_name(), self.user.phone, self.lead_instance.client.name, self.lead_instance.client.phone)
        data = {
            'author': self.user,
            'type': 'vehicle_information',
            'description': description,
            'is_click2call': True
        }
        self._set_realization_or_traking(data=data)
        return super().validate(data)

    def create(self, validated_data):
        response = Client().post(
            telefono=self.lead_instance.client.phone.replace('+', ''), memberid=self.user.memberid, idcliente=self.user.id_click2call)
        if response['status']:
            task_instance = super().create(validated_data)
            self._set_lead_status(task_instance)
            return task_instance
        else:
            raise ValidationError(response['message'])

    def update(self, instance, validated_data):
        raise NotImplementedError()

