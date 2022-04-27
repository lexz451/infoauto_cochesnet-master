# -*- coding: utf-8 -*-

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from infoauto.leads.models import GasType, Vehicle, VehicleBrand, VehicleVersion, VehicleModel
from infoauto.leads.serializers.origins import OriginSerializer
from infoauto.source_channels.serializers.channels import ChannelSerializer


class GasTypeSerializer(WritableNestedModelSerializer):
    class Meta:
        model = GasType
        fields = ('id', 'name', )


class VehicleBrandSerializer(ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = ('id', 'name',)


class VehicleModelSerializer(ModelSerializer):

    brand = VehicleBrandSerializer()

    class Meta:
        model = VehicleModel
        fields = ('id', 'model_name', 'brand')


class VehicleVersionSerializer(ModelSerializer):

    vehicle_model = VehicleModelSerializer()
    gas_type_data = GasTypeSerializer(source='gas_type', read_only=True)

    version_fullname = SerializerMethodField()

    def get_version_fullname(self, obj):
        return "{0} - ({1} - {2})".format(obj.version_name, obj.fuel, obj.engine_power)

    class Meta:
        model = VehicleVersion
        fields = (
            'id', 'version_name', 'motor', 'engine_power',
            'fuel', 'gearbox', 'vehicle_model',
            'comments', 'size', 'gas_type_data',
            'version_fullname'
        )


class HisoricalVehicleSerializer(WritableNestedModelSerializer):
    gas_data = GasTypeSerializer(read_only=True, source='gas')

    class Meta:
        model = apps.get_model('leads', model_name='HistoricalVehicle')
        fields = (
            'id', 'lead', 'brand_model', 'price', 'km', 'year', 'gas', 'gas_data', 'vehicle_type',
            'comercial_category', 'power', 'gear_shift', 'ad_link', 'history_id', 'history_change_reason', 'history_date',
            'history_user', 'history_type'
        )
        extra_kwargs = {'lead': {'read_only': True, 'required': False}}


class VehicleSerializer(WritableNestedModelSerializer):
    gas_data = GasTypeSerializer(read_only=True, source='gas')
    # history = HisoricalVehicleSerializer(read_only=True, many=True)
    #origin_data = OriginSerializer(source='origin', read_only=True)
    #media_data = ChannelSerializer(source='media', read_only=True)

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'lead',
            'brand_model',
            'vehicle_type',
            'comercial_category',
            'power',
            'gear_shift',
            'ad_link',
            'model',
            'version',
            'price',
            'km',
            'year',
            'gas',
            'gas_data',
            'note',
            'number_vehicles',
            'segment',
            'purchase_method',
            'purchase_description',
            'initial_payment',
            'financial_term',
            'finalcial_km_year',
            'maximum_monthlyfee',
            'pff',
            'percent_comision',
            'total_commision',
            'oportunity_state',
            'rejection_reason',
            'price_discount'
        )
        extra_kwargs = {
            'gas_data': {'read_only': True},
            'brand_model': {
                'required': False, 'allow_null': True,
                'allow_blank': False
            }
        }

    def create(self, validated_data):
        # available_origins = validated_data['lead'].concessionaire.source_set.all().values_list('origin', flat=True)
        # if validated_data.get('origin') and validated_data['origin'].id not in available_origins:
        #     raise ValidationError({'origin': _("Origen no disponible")})
        # if validated_data.get('media'):
        #     if not validated_data.get('origin'):
        #         raise ValidationError({'media': _("Se requiere un origen para establecer el medio")})
        #     elif validated_data['media'] not in validated_data['origin'].available_channels.all():
        #         raise ValidationError({'media': _("El medio no está disponible")})
        return super().create(validated_data)

