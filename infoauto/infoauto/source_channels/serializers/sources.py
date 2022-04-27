from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty, SerializerMethodField, BooleanField, CharField

from infoauto.common.serializers import Base64FileField
from infoauto.leads.models import Origin, Concessionaire
from infoauto.leads.models.common import phone_regex
from infoauto.leads.serializers.notes import NoteSerializer
from infoauto.source_channels.models import Source
from infoauto.source_channels.serializers.channels import ChannelSerializer
from infoauto.users.models import User
from infoauto.users.serializers.sessions_historic import SessionWithHistoricSerializer
from infoauto.work_calendar.serializers import WeekSerializer



class SimpleOriginSerializer(WritableNestedModelSerializer):
    icon = Base64FileField(header='data:image')
    available_channels_data = ChannelSerializer(many=True, read_only=True, source='available_channels')

    class Meta:
        model = Origin
        fields = ('id', 'name', 'icon', 'available_channels', 'available_channels_data')


class BaseSourceSerializer(WritableNestedModelSerializer):
    channel_data = ChannelSerializer(source="channel", read_only=True)
    origin_data = SimpleOriginSerializer(source='origin', read_only=True)

    class Meta:
        model = Source
        fields = ('id', 'channel', 'channel_data', 'data', 'origin', 'origin_data', 'concession')

    def origin_channel_compatibility(self, attrs):
        if attrs.get('origin', getattr(self.instance, 'origin', None)).available_channels.all() and\
                (attrs.get('channel', getattr(self.instance, 'channel', None)) not in
                 attrs.get('origin', getattr(self.instance, 'origin', None)).available_channels.all()):
            raise ValidationError({'channel': _("This channel is not compatible with the origin")})

    def required_data(self, attrs):
        if attrs.get("channel", getattr(self.instance, 'channel', None)).slug in \
                getattr(settings, 'REQUIRED_SOURCE_DATA', ['email', 'phone']):
            if not attrs.get('data', getattr(self.instance, 'data', None)):
                raise ValidationError({'data': _("This field is required")})

    def phone_duplicated(self, phone):
        if not self.instance or (self.instance and self.instance.data != phone):
            slug = getattr(settings, 'BASE_PHONE_SLUG', 'phone')
            if self.Meta.model.objects.filter(data=phone, channel__slug=slug).exists():
                raise ValidationError({'data': _("This phone already exists")})

    def data_validation(self, attrs):
        channel_slug = attrs.get('channel', getattr(self.instance, 'channel', None)).slug
        if channel_slug == 'phone':
            phone = attrs.get('data', getattr(self.instance, 'data', None))
            try:
                phone_regex.__call__(phone)
            except DjangoValidationError:
                raise ValidationError({'data': _("This field is not a phone")})
            self.phone_duplicated(phone)
        elif channel_slug == 'email':
            email = attrs.get('data', getattr(self.instance, 'data', None))
            try:
                validate_email(email)
            except DjangoValidationError:
                raise ValidationError({'data': _("This field is not an email")})

    def run_validation(self, data=empty):
        if data.get('id'):
            try:
                self.instance = self.Meta.model.objects.get(id=data['id'])
            except self.Meta.model.DoesNotExist:
                self.instance = None
        return super().run_validation(data=data)

    def uniqueness_validation(self, attrs):
        data = attrs.get("data")
        origin = attrs.get("origin")
        channel = attrs.get("channel")
        kwargs = {'channel': channel, 'origin': origin, 'data': data}
        from infoauto.concessionaires.views import ConcessionaireView
        if isinstance(self.context.get('view'), ConcessionaireView):
            try:
                concession = self.context['view'].get_object()
            except AssertionError:
                concession = None
            if concession:
                kwargs.update({'concession': concession})
                try:
                    aux_instance = self.Meta.model.objects.get(**kwargs)
                    if self.instance != aux_instance:
                        raise ValidationError({'data': _("Source already exists"), 'origin': _("Source already exists"),
                                               'channel': _("Source already exists")})
                except self.Meta.model.DoesNotExist:
                    pass
        return True

    def validate(self, attrs):
        self.required_data(attrs)
        self.origin_channel_compatibility(attrs)
        self.data_validation(attrs)
        self.uniqueness_validation(attrs)
        return super().validate(attrs)


class SourceSerializer(BaseSourceSerializer):
    concession_data__name = CharField(read_only=True, source='concession_name')

    class Meta:
        model = Source
        fields = ('id', 'channel', 'channel_data', 'data', 'origin', 'origin_data', 'concession_data__name')


class SimpleUserSerializer(WritableNestedModelSerializer):
    is_admin = BooleanField(read_only=True)
    is_concession_admin = BooleanField(read_only=True)
    is_business_manager = BooleanField(read_only=True)
    session = SessionWithHistoricSerializer(read_only=True, allow_null=True, source='sessionwithhistoric')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'username', 'email',
                  'is_staff', 'is_superuser', 'is_admin', 'is_concession_admin',
                  'is_business_manager', 'is_active', 'session', 'user_activation_date', 'user_deactivation_date')
        read_only_fields = fields


class SimpleConcessionaireSerializer(WritableNestedModelSerializer):
    work_calendar = WeekSerializer(required=False, allow_null=True)
    sources = SourceSerializer(many=True, source="source_set")
    notes_data = NoteSerializer(many=True, read_only=True, source='notes')
    related_users = SimpleUserSerializer(source='user', many=True)

    class Meta:
        model = Concessionaire
        fields = ('id', 'name', 'address', 'latitude', 'longitude', 'schedule', 'web',
                  'web_coches_net', 'date_notes', 'appraisal_notes', 'financing_notes', 'warranty_notes',
                  'service_notes', 'work_calendar', 'sources', 'notes_data', 'related_users')
        read_only_fields = fields


class CompleteSourceSerializer(BaseSourceSerializer):
    concession_data = SimpleConcessionaireSerializer(read_only=True, source='concession')

    class Meta:
        model = Source
        fields = ('id', 'channel', 'channel_data', 'data', 'origin', 'origin_data', 'concession', 'concession_data')

    def to_representation(self, instance):
        view = self.context.get("view")
        if view and view.action not in ['retrieve']:
            try:
                self.fields['concession_data'].fields.pop('work_calendar', None)
            except:
                pass
            try:
                self.fields['concession_data'].fields.pop('sources', None)
            except:
                pass
            try:
                self.fields['concession_data'].fields.pop('notes_data', None)
                self.fields['concession_data'].fields.pop('related_users', None)
            except:
                pass
            try:
                self.fields['origin_data'].fields.pop('available_channels', None)
                self.fields['origin_data'].fields.pop('available_channels_data', None)
            except:
                pass
        return super().to_representation(instance)
