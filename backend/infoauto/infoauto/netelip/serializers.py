from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.fields import FloatField, SerializerMethodField, CharField

from infoauto.netelip.models import CallControlModel


class CallControlSerializer(serializers.ModelSerializer):
    ID = FloatField(source='id_call')
    simple_status = CharField(read_only=True)

    class Meta:
        model = CallControlModel
        fields = (
            "id",
            "ID",
            "api",
            "src",
            "dst",
            "startcall",
            "durationcall",
            "durationcallanswered",
            "command",
            "options",
            "description",
            "dtmf",
            "statuscode",
            "statuscall",
            "userdata",
            "typesrc",
            "usersrc",
            "call_origin",
            "has_audio",
            "simple_status"
        )

