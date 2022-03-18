
from email.policy import default
from infoauto.vehicles.serializers import GasTypeSerializer, VehicleBrandSerializer, VehicleModelSerializer
from infoauto.source_channels.serializers.sources import SourceSerializer, ChannelSerializer
from infoauto.leads.serializers.origins import OriginSerializer
from drf_writable_nested import WritableNestedModelSerializer
from infoauto.source_channels.models import Source, Channel
from infoauto.leads.models import Campaign, Concessionaire, Origin, VehicleBrand, VehicleModel, VehicleVersion
from rest_framework.fields import DateTimeField, CharField, SerializerMethodField, BooleanField


class CampaignConcessionarySerializer(WritableNestedModelSerializer):
    class Meta:
        model = Concessionaire
        fields = ['id', 'name']


class CampaignOriginSerializer(WritableNestedModelSerializer):
    available_channels = ChannelSerializer(many=True, read_only=True)

    class Meta:
        model = Origin
        fields = ['id', 'name', 'available_channels']


class CampaignSourceSerializer(WritableNestedModelSerializer):
    name = SerializerMethodField(read_only=True)

    def get_name(self, source):
        return r'XXX'

    class Meta:
        model = Source
        fields = ['id', 'name']


class CampaignBrandSerializer(WritableNestedModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = ['id', 'name']


class CampaignModelSerializer(WritableNestedModelSerializer):
    name = SerializerMethodField(read_only=True)
    brand = VehicleBrandSerializer()

    def get_name(self, model):
        return r'Model...'

    class Meta:
        model = VehicleModel
        fields = ['id', 'name', 'model_name', 'brand']


class CampaignVersionSerializer(WritableNestedModelSerializer):
    name = SerializerMethodField(read_only=True)
    vehicle_model = VehicleModelSerializer(read_only=True)
    gas_type = GasTypeSerializer(read_only=True)
    #version_fullname = SerializerMethodField()

    def get_name(self, model):
        return r'Model...'

    class Meta:
        model = VehicleVersion
        fields = ['id', 'name', 'size', 'version_name', 'motor', 'engine_power',
                  'fuel', 'gearbox', 'comments', 'vehicle_model', 'gas_type']


class CampaignSerializer(WritableNestedModelSerializer):
    concessionaire = CampaignConcessionarySerializer(allow_null=True, required=False)
    origin = CampaignOriginSerializer(allow_null=True, required=False)
    source = CampaignSourceSerializer(allow_null=True, required=False)
    brand = CampaignBrandSerializer(allow_null=True, required=False)
    model = CampaignModelSerializer(allow_null=True, required=False)
    version = CampaignVersionSerializer(allow_null=True, required=False)
    channel = ChannelSerializer(allow_null=True, required=False)

    class Meta:
        model = Campaign
        partial = True
        fields = [
            'id',
            'name',
            'concessionaire',
            'origin', 'source',
            'brand',
            'model',
            'version',
            'investment',
            'url',
            'offer',
            'note',
            'status',
            'communicationType',
            'campaignType',
            'channel',
            'expenses',
            'utm_campaign',
            'utm_source',
            'utm_content',
            'campaingId'
        ]
