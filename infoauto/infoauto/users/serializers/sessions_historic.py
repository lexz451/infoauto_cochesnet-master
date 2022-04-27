from django.apps import apps
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from infoauto.users.models import SessionWithHistoric


class SessionWithHistoricSerializer(WritableNestedModelSerializer):
    # history = HistoricalSessionWithHistoricSerializer(read_only=True, many=True)
    online = serializers.BooleanField(read_only=True)

    class Meta:
        model = SessionWithHistoric
        fields = ("id", "start_working", "last_seen", "online")


class SimpleSessionWithHistoricSerializer(WritableNestedModelSerializer):
    class Meta:
        model = SessionWithHistoric
        fields = ('id', 'forced_online_status')
        read_only_fields = fields

    def update(self, instance, validated_data):
        validated_data['forced_online_status'] = not instance.forced_online_status
        return super().update(instance, validated_data)


class HistoricalSessionWithHistoricSerializer(WritableNestedModelSerializer):
    class Meta:
        model = apps.get_model('users', model_name='HistoricalSessionWithHistoric')
        # fields = (i.name for i in HistoricalNote._meta.fields)
        fields = ("history_id", "modified", "start_working", "end_working")
        read_only_fields = fields
