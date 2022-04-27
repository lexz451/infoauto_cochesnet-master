import json
from json import JSONDecodeError

from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
from drf_yasg.utils import swagger_serializer_method
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from infoauto.concessionaires.serializers import SimpleConcessionarie
from infoauto.expanded_settings.settings import settings
from infoauto.leads.serializers import LeadColumnSerializer
from infoauto.netelip.client import APIVoiceClient, Click2CallUbunetClient
from infoauto.leads.models import Lead, Concessionaire
from infoauto.netelip.models import Flow, Command, CallControlModel
from infoauto.netelip.serializers import CallControlSerializer as BaseCallControlSerializer
from infoauto.netelip_leads.models import CallControlLeadModel
from infoauto.source_channels.models import Source
from infoauto.source_channels.serializers import SourceSerializer
from infoauto.users.models import User
from infoauto.users.serializers.users import SimplestUserSerializer


class CallControlLeadSerializer(WritableNestedModelSerializer):

    class Meta:
        model = CallControlLeadModel
        fields = ('id', 'call_control', 'lead')


class CallControlSerializer(BaseCallControlSerializer):
    callcontrolleadmodel = CallControlLeadSerializer(read_only=True)
    possible_leads = SerializerMethodField()
    concessionaire = SerializerMethodField()
    source = SerializerMethodField()
    user = SerializerMethodField()

    class Meta(BaseCallControlSerializer.Meta):
        new_fields = ('callcontrolleadmodel', 'possible_leads', 'concessionaire', 'source', 'user')
        fields = BaseCallControlSerializer.Meta.fields + new_fields

    @swagger_serializer_method(serializer_or_field=LeadColumnSerializer)
    def get_possible_leads(self, obj):

        try:
            if obj.callcontrolleadmodel and obj.callcontrolleadmodel.lead:
                return None
        except CallControlLeadModel.DoesNotExist:
            pass
        queryset = Lead.objects.filter(~Q(status__in=['end']), client__phone=obj.src, source__data__icontains=obj.dst).distinct().order_by('id')
        return LeadColumnSerializer(queryset, many=True).data

    @swagger_serializer_method(serializer_or_field=SimpleConcessionarie)
    def get_concessionaire(self, obj):
        try:
            concession = Concessionaire.objects.get(source__data=obj.dst)
            return SimpleConcessionarie(instance=concession).data
        except Concessionaire.DoesNotExist:
            return None

    @swagger_serializer_method(serializer_or_field=SimplestUserSerializer)
    def get_user(self, obj):
        if obj.ubunet_agent:
            try:
                user = User.objects.get(ubunet_agent=obj.ubunet_agent)
                return SimplestUserSerializer(instance=user).data
            except User.DoesNotExist:
                user = User.objects.filter(phone=obj.ubunet_agent).first()
                if not user:
                    return None
                return SimplestUserSerializer(instance=user).data

        else:
            return None

    @swagger_serializer_method(serializer_or_field=SourceSerializer)
    def get_source(self, obj):
        try:
            source = Source.objects.get(data=obj.dst)
            return SourceSerializer(instance=source).data
        except Source.DoesNotExist:
            return None


class Click2CallSerializer(WritableNestedModelSerializer):
    class Meta:
        model = CallControlLeadModel
        fields = ('id', 'lead', 'call_control', 'user')
        read_only_fields = ('id', 'call_control', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lead_instance = None

    def validate(self, attrs):
        self.lead_instance = attrs['lead']
        attrs['user'] = self.context['request'].user
        return super().validate(attrs)

    @staticmethod
    def get_flow():
        try:
            flow_instance = Flow.objects.get(is_default=True, type='c2c')
        except Flow.DoesNotExist:
            raise ValidationError(_("Error en la configuración"))
        return flow_instance

    def get_command(self):
        flow_instance = self.get_flow()
        try:
            first_step = flow_instance.command_set.get(is_initial=True)
        except Command.DoesNotExist:
            raise ValidationError(_("Error en la configuración del flujo"))
        return first_step

    def _get_c2c_from_lead(self):
        if self.lead_instance:
            return self.lead_instance.callcontrolleadmodel_set.filter(call_control__call_origin='user').exists()
        return False

    def _set_lead_status(self):
        c2c_exists = self._get_c2c_from_lead()
        if self.lead_instance.status in ['new', 'pending', 'commercial_management']:
            setattr(self.lead_instance, 'force_status', True)
            if not c2c_exists:
                self.lead_instance.status = 'commercial_management'
            self.lead_instance.save()

    @staticmethod
    def _get_id_call(response, validated_data):
        try:
            id_call = json.loads(response.content).get("ID", None)
        except (JSONDecodeError, TypeError, ):
            id_call = None
        return id_call

    def create(self, validated_data):

        user_phone = self.context['request'].user.phone
        user_ubunet_extension = self.context['request'].user.ubunet_extension
        user_ubunet_company = self.context['request'].user.ubunet_company

        if user_ubunet_extension and user_ubunet_company:
            try:
                client = Click2CallUbunetClient()

                client.c2c(
                    company=user_ubunet_company,
                    extension=user_ubunet_extension,
                    phone=self.lead_instance.client.phone  # .replace('+', '00')
                )
            except Exception as e:
                raise ValidationError(e)

        else:
            client = APIVoiceClient()
            flow = self.get_flow()
            first_step = self.get_command()
            if not user_phone:
                raise ValidationError("El teléfono del usuario no ha sido especificado")
            try:
                response = client.internal_c2c(
                    flow_id=flow.id, first_step=first_step.id,
                    phone_orig=user_phone.replace('+', '00'),
                    type_phone_orig="pstn", phone_dest=self.lead_instance.client.phone.replace('+', '00'),
                    src=self.lead_instance.concessionaire.mask_c2c.replace('+', '00'), duration=60)
            except Exception as e:
                raise ValidationError(e)
            id_c2c = self._get_id_call(response=response, validated_data=validated_data)
            data = {
                'id_call': id_c2c,
                'api': settings.NETELIP_API_NAME,
                'src': self.lead_instance.concessionaire.mask_c2c,
                'startcall': timezone.now()
            }
            validated_data['call_control'] = CallControlModel.objects.create(**data)

        instance = super().create(validated_data)
        return instance

