# -*- coding: utf-8 -*-
import datetime

from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from infoauto.common.util_email import send_email
from infoauto.concessionaires.serializers import WUUserConcessionSerializer
from infoauto.leads.models import Lead, Concessionaire

from infoauto.users.models import User, UserSFA
from infoauto.users.serializers.sessions_historic import SessionWithHistoricSerializer

from infoauto.users.models import UserWhatsappTemplate


class UserSFASerializer(WritableNestedModelSerializer):

    channel = serializers.CharField(required=True, allow_blank=False)
    event = serializers.CharField(required=True, allow_blank=False)
    text = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = UserSFA
        fields = ('id', 'user', 'channel', 'event', 'text')


class UserWhatsappTemplateSerializer(WritableNestedModelSerializer):

    text = serializers.CharField(required=True, allow_blank=False)
    alias = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = UserWhatsappTemplate
        fields = ('id', 'user', 'text', 'alias')


class SimplestUserSerializer(WritableNestedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'username', 'email', 'is_online', 'lost_calls', 'emails_received')


class SimpleUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'username', 'email', 'is_online', 'lost_calls',
                  'emails_received', 'is_available', 'today_lead_number', 'last_lead_datetime', 'unattended_leads',
                  'delayed_tasks', 'delayed_trackings')


class SetPassword(object):

    def update_user_password(self, user, password=None, request=None):
        password = password or User.objects.make_random_password()
        user.set_password(password)
        user.save()
        print('Username: %s; Password: %s' % (user.email, password))
        # SEND MAIL PASSWORD
        context = {'user': user, 'password': password, 'domain_url': 'https://sail.artificialintelligencelead.com/'}
        #send_email(to_email=[user.email],
        #           subject=getattr(settings, 'EMAIL_SUBJECT', _('Solicitud de nueva contraseña')),
        #           template='email/password', context=context, request=request,
        #           smtp_config_name="default")
        return user


class UserCreateSerializer(serializers.ModelSerializer, SetPassword):
    repeat_password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone',
            'email',
            'memberid',
            'id_click2call',
            'password',
            'repeat_password'
        )
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        returned = super().validate(attrs)
        if returned.get('password') != returned.get('repeat_password'):
            raise ValidationError(_("Those passwords don't match."))
        return returned

    def create(self, validated_data):
        password = validated_data['password']
        validated_data.pop('repeat_password', None)
        self.data.pop('repeat_password', None)
        validated_data['username'] = validated_data['email']
        instance = super().create(validated_data)
        if instance:
            instance = self.update_user_password(instance, password)
        return instance


class SFAUserUpdateSerializer(WritableNestedModelSerializer, SetPassword):
    sfa_configurations = UserSFASerializer(many=True, required=False, allow_null=True)
    whatsapp_templates = UserWhatsappTemplateSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'sfa_configurations', 'whatsapp_templates'
        )


class ComplexUserCreateSerializer(WritableNestedModelSerializer, SetPassword):
    remove_concessions = False
    repeat_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    related_concessionaires = WUUserConcessionSerializer(
        many=True, required=False, allow_null=True, source='userconcession_set'
    )

    sfa_configurations = UserSFASerializer(many=True, required=False, allow_null=True)
    whatsapp_templates = UserWhatsappTemplateSerializer(many=True, required=False, allow_null=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_concession_admin = serializers.BooleanField(read_only=True)
    is_business_manager = serializers.BooleanField(read_only=True)
    session = SessionWithHistoricSerializer(read_only=True, allow_null=True, source='sessionwithhistoric')

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'phone', 'memberid', 'id_click2call', 'username', 'email',
            'password', 'repeat_password', 'is_staff', 'is_superuser', 'related_concessionaires', 'is_admin',
            'is_concession_admin', 'is_business_manager', 'is_active', 'session', 'user_activation_date',
            'user_deactivation_date', 'is_available','unavailable_reason', 'today_lead_number', 'is_online',
            'last_lead_datetime', 'sfa_configurations', 'whatsapp_templates', 'lost_calls', 'emails_received', 'ddi_whatsapp_business',
            'ubunet_extension', 'ubunet_company', 'ubunet_agent'
        )
        extra_kwargs = {
            'email': {'required': True}, 'username': {'read_only': True},
            'password': {'write_only': True, 'required': False, 'allow_blank': True},
            'user_activation_date': {'read_only': True}, 'user_deactivation_date': {'read_only': True},
            'is_available': {'required': False},
            'unavailable_reason': {'required': False}
        }

    def __init__(self, *args, **kwargs):
        self.related_concessionaires = WUUserConcessionSerializer(
            many=True, required=False, allow_null=True, source='userconcession_set',
            context=kwargs.get("context", {}))
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        current_user = self.context['request'].user
        if self.instance and not current_user.is_admin and self.instance.is_admin:
            raise ValidationError(_("No tienes permisos suficientes para modificar este usuario"))
        if attrs.get('password', '') != attrs.get('repeat_password', ''):
            raise ValidationError(_("Those passwords don't match."))
        if self.instance and attrs.get('is_active') is False and self.instance.is_active is True:
            if self.instance.lead_set.all().exists():
                raise ValidationError({'is_active': _("Este usuario no puede ser dado de baja en la plataforma."
                                                      " Aún tiene leads asignados.")})
            else:
                self.remove_concessions = True
        return super().validate(attrs)

    def update_or_create(self, validated_data):
        password = validated_data.get('password')
        validated_data.pop('repeat_password', None)
        self.fields.pop('repeat_password', None)
        email = validated_data.get('email')
        validated_data.update({'username': email}) if email else None
        return password

    def create(self, validated_data):
        password = self.update_or_create(validated_data)
        instance = super().create(validated_data)
        if instance and password:
            instance = self.update_user_password(instance, password)
        return instance

    def update(self, instance, validated_data):
        password = self.update_or_create(validated_data)
        instance = super().update(instance, validated_data)
        self.update_user_password(instance, password) if password else None
        instance.userconcession_set.all().delete() if self.remove_concessions else None
        return instance

    def delete_reverse_relations_if_need(self, instance, reverse_relations):
        pass

    def to_representation(self, instance):
        try:
            self.fields['related_concessionaires'].child.fields.pop('related_uesers', None)
            self.fields['related_concessionaires'].child.fields.pop('work_calendar', None)
            self.fields['related_concessionaires'].child.fields.pop('sources', None)
            self.fields['related_concessionaires'].child.fields.pop('notes', None)
            self.fields['related_concessionaires'].child.fields.pop('notes_data', None)
        except:
            pass
        return super().to_representation(instance)


class SetUserLeadsSerializer(WritableNestedModelSerializer):
    leads = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all(), many=True, source='lead_set', required=True)

    class Meta:
        model = User
        fields = ('id', 'leads')

    def validate(self, attrs):
        concession_queryset = Concessionaire.objects.filter(id__in=[i.concessionaire.id for i in attrs['lead_set']])
        user_concessions = self.instance.userconcession_set.all().values_list('concessionaire', flat=True)
        for concession in concession_queryset:
            if concession.id not in user_concessions:
                raise ValidationError({
                    'leads': _("Algunos de los leads no pueden ser asignados al usuario seleccionado."
                               " Por favor, póngase en contacto con el Departamento de Atención al Cliente")})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.lead_set.add(*validated_data['lead_set'])
        return instance


