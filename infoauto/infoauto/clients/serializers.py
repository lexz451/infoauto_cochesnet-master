from django.apps import apps
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.fields import CharField

from infoauto.business_activity.business_activity_serializers import BusinessActivitySerializer, BusinessSectorSerializer
from infoauto.countries.serializers import ProvinceSerializer, LocalitySerializer
from infoauto.leads.models import Client
from infoauto.users.serializers.users import SimplestUserSerializer


class HistoricalClientSerializer(WritableNestedModelSerializer):
    history_user = CharField(source='history_user.username', default=None)

    class Meta:
        model = apps.get_model('leads', model_name='HistoricalClient')
        fields = [
            'id',
            'created',
            'modified',
            'name',
            'phone',
            'email',
            'province',
            'location',
            'client_type',
            'business_name',
            'identification',
            'desk_phone',
            'address1',
            'address2',
            'history_id',
            'history_change_reason',
            'history_date',
            'history_user',
            'history_type',
        ]


class ClientSerializer(WritableNestedModelSerializer):
    province_data = ProvinceSerializer(read_only=True, source='province')
    location_data = LocalitySerializer(read_only=True, source='location')
    user = SimplestUserSerializer(read_only=True)

    business_activity_data = BusinessActivitySerializer(read_only=True, source='business_activity')
    sector_data = BusinessSectorSerializer(read_only=True, source='sector')

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'surname',
            'postal_code',
            'phone',
            'email',
            'province',
            'province_data',
            'location',
            'location_data',
            'user',
            'client_type',
            'business_name',
            'business_activity',
            'sector',
            'business_activity_data',
            'sector_data',
            'position',
            'identification',
            'desk_phone',
            'address1',
            'address2',
            'segment',
            'fleet'
        )

        read_only_fields = ('user', 'created')

    def to_representation(self, instance):
        view = self.context.get('view')
        if view and view.action not in ["retrieve"]:
            self.fields.pop("history", None)
        return super().to_representation(instance)
