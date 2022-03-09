import base64

import six
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import get_object_or_404

from infoauto.leads.models import UserConcession, Concessionaire, Phone, Email, Origin
from infoauto.leads.serializers.notes import NoteSerializer
from infoauto.source_channels.serializers import SourceSerializer
from infoauto.users.models import User
from infoauto.work_calendar.serializers import WeekSerializer


class Base64FileField(serializers.FileField):
    def __init__(self, header='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = header

    def to_internal_value(self, data):
        if isinstance(data, six.string_types) and data.startswith(self.header):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class SimpleOriginSerializer(WritableNestedModelSerializer):
    icon = Base64FileField(header='data:image')

    class Meta:
        model = Origin
        fields = ('id', 'name', 'icon')


class PhoneSerializer(WritableNestedModelSerializer):
    origin_data = SimpleOriginSerializer(source='origin', read_only=True)

    class Meta:
        model = Phone
        fields = ('id', 'number', 'origin', 'origin_data')

    def to_internal_value(self, data):
        """
        Pop number if current phone has de same. UniqueValidators does not include Instance to check if same value.
        :param data: Dictionary with instance data.
        :return: ret: Dictionary with validated data.
        """
        if data.get("id"):
            instance = get_object_or_404(queryset=Phone.objects.all(), id=data['id'])
            if data.get('number') and instance.number == data['number']:
                data.pop('number', None)
        return super().to_internal_value(data=data)


class ListPhoneSerializer(serializers.ModelSerializer):
    origin_data = SimpleOriginSerializer(source='origin', read_only=True)
    concession_id = SerializerMethodField(read_only=True)
    concession_name = SerializerMethodField(read_only=True)

    class Meta:
        model = Phone
        fields = ('id', 'number', 'origin', 'origin_data', 'concession_id', 'concession_name')
        read_only_fields = fields

    def _get_concession(self, obj):
        concession = obj.concessionaire_set.all().first()
        return concession

    def get_concession_name(self, obj):
        concession = self._get_concession(obj)
        return concession.name if concession else None

    def get_concession_id(self, obj):
        concession = self._get_concession(obj)
        return concession.id if concession else None


class EmailSerializer(WritableNestedModelSerializer):
    origin_data = SimpleOriginSerializer(source='origin', read_only=True)

    class Meta:
        model = Email
        fields = ('id', 'email', 'origin', 'origin_data')

    def to_internal_value(self, data):
        """
        Pop number if current phone has de same. UniqueValidators does not include Instance to check if same value.
        :param data: Dictionary with instance data.
        :return: ret: Dictionary with validated data.
        """
        if data.get("id"):
            instance = get_object_or_404(queryset=Email.objects.all(), id=data['id'])
            if data.get('email') and instance.email == data['email']:
                data.pop('email', None)
        return super().to_internal_value(data=data)


class ListEmailSerializer(serializers.ModelSerializer):
    origin_data = SimpleOriginSerializer(source='origin', read_only=True)
    concession_id = SerializerMethodField(read_only=True)
    concession_name = SerializerMethodField(read_only=True)

    class Meta:
        model = Email
        fields = ('id', 'email', 'origin', 'origin_data', 'concession_id', 'concession_name')
        read_only_fields = fields

    def _get_concession(self, obj):
        concession = obj.concessionaire_set.all().first()
        return concession

    def get_concession_name(self, obj):
        concession = self._get_concession(obj)
        return concession.name if concession else None

    def get_concession_id(self, obj):
        concession = self._get_concession(obj)
        return concession.id if concession else None


class UserConcessionSerializer(WritableNestedModelSerializer):
    class Meta:
        model = UserConcession
        fields = ('id', 'user', 'concessionaire', 'is_concessionaire_admin', 'is_business_manager')


class WCUserConcessionSerializer(UserConcessionSerializer):
    """
    UserConcession serializer without Concession field
    """
    # relation_id = PrimaryKeyRelatedField(queryset=UserConcession.objects.all(), source='id', required=False)
    class BasicUserSerializer(serializers.ModelSerializer):
        online = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = ('id', 'first_name', 'last_name', 'username', 'phone', 'email', 'online')

        def get_online(self, obj):
            try:
                swh = obj.sessionwithhistoric
            except Exception:
                swh = None
            return getattr(swh, 'online', False)

    user_data = BasicUserSerializer(read_only=True, source='user')

    class Meta:
        model = UserConcession
        fields = ('id', 'user', 'user_data', 'is_concessionaire_admin', 'is_business_manager')


class SimpleConcessionaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concessionaire
        fields = ('id', 'name', 'address', 'web',)

    def delete_reverse_relations_if_need(self, instance, reverse_relations):
        pass

class ConcessionaireSerializer(WritableNestedModelSerializer):
    related_users = WCUserConcessionSerializer(many=True, required=False, allow_null=True, source='userconcession_set')
    work_calendar = WeekSerializer(required=False, allow_null=True)
    sources = SourceSerializer(many=True, source='source_set')
    notes_data = NoteSerializer(source='notes', many=True, required=False, allow_null=True)

    class Meta:
        model = Concessionaire
        fields = ('id', 'name', 'address', 'latitude', 'longitude', 'schedule', 'web',
                  'web_coches_net', 'date_notes', 'appraisal_notes', 'financing_notes', 'warranty_notes',
                  'service_notes', 'related_users', 'work_calendar', 'sources', 'notes', 'notes_data',
                  'mask_c2c', 'concession_phone', 'hubspot_api_key', 'hubspot_id')

    def delete_reverse_relations_if_need(self, instance, reverse_relations):
        pass


class WUUserConcessionSerializer(UserConcessionSerializer):
    """
    UserConcession serializer without User field
    """
    # relation_id = PrimaryKeyRelatedField(queryset=UserConcession.objects.all(), source='id', required=False)
    concessionaire_data = ConcessionaireSerializer(source='concessionaire', read_only=True)

    class Meta:
        model = UserConcession
        fields = ('id', 'concessionaire', 'concessionaire_data', 'is_concessionaire_admin',
                  'is_business_manager')

    def to_representation(self, instance, *args, **kwargs):
        if self.context.get('view') and self.context['view'].__class__.__name__ == 'UserView':
            self.fields['concessionaire_data'].fields.pop('related_users', None)
            self.fields['concessionaire_data'].fields.pop('notes', None)
            self.fields['concessionaire_data'].fields.pop('notes_data', None)
        return super().to_representation(instance)

    def is_valid(self, raise_exception=False):
        concessionaire_id = self.initial_data.get('concessionaire', None)
        current_id = self.initial_data.get('id') or self.initial_data.get('pk')
        view = self.context.get('view')
        if concessionaire_id and not current_id:
            try:
                queryset = view.get_object().userconcession_set.filter(concessionaire__id=concessionaire_id)
                if queryset:
                    raise ValidationError(
                        _("No puedes escoger el mismo concesionario en mas de una ocasión")
                    )
            except AssertionError:
                """
                When new user is created. Can't take instance from models.
                """
                pass
        request = self.context.get('request')
        if request and request.method in ['POST', 'PATCH', 'PUT'] and not [i for i in self.initial_data.values() if i]:
            raise ValidationError(_("No se admiten concesionarios vacíos"))
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        current_user = self.context['request'].user
        if not current_user.is_admin:
            if not current_user.userconcession_set.filter(
                    is_concessionaire_admin=True, concessionaire=attrs['concessionaire']).exists():
                raise ValidationError({
                    'concessionaire': _("No tiene permisos para realizar dicha acción."
                                        "Usted no pertenece y/o administra esta concesión")
                })
        return super().validate(attrs)


class SimpleConcessionarie(WritableNestedModelSerializer):
    class Meta:
        model = Concessionaire
        fields = ('id', 'name')


class ConcessionDashboardSerializer(SimpleConcessionarie):
    iframe_content = serializers.CharField(source='schedule')

    class Meta(SimpleConcessionarie.Meta):
        fields = SimpleConcessionarie.Meta.fields + ('iframe_content', )
