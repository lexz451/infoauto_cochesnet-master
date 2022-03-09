from drf_writable_nested import WritableNestedModelSerializer

from infoauto.common.serializers import Base64FileField
from infoauto.leads.models import Origin, Phone, Email
from infoauto.source_channels.serializers.channels import ChannelSerializer


class BasePhoneSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'number')


class BaseEmailSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Email
        fields = ('id', 'email')


class OriginSerializer(WritableNestedModelSerializer):
    phone_set = BasePhoneSerializer(many=True, read_only=True)
    email_set = BaseEmailSerializer(many=True, read_only=True)
    icon = Base64FileField(header='data:image')
    available_channels_data = ChannelSerializer(many=True, read_only=True, source='available_channels')

    class Meta:
        model = Origin
        fields = ('id', 'name', 'icon', 'phone_set', 'email_set', 'available_channels', 'available_channels_data')


