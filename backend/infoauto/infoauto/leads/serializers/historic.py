from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField


class HistorySerializer(serializers.Serializer):
    history_date = DateTimeField()
    history_user = CharField(source='history_user.username')
    history_change_reason = CharField()
    history_type = CharField()

    class Meta:
        fields = ('history_date', 'history_user', 'history_change_reason', 'history_type')
