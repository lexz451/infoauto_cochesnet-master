from django.apps import apps
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.fields import SerializerMethodField

from infoauto.leads.models import Note


class HisoricalNoteSerializer(WritableNestedModelSerializer):
    class Meta:
        model = apps.get_model('leads', model_name='HistoricalNote')
        # fields = [i.name for i in HistoricalNote._meta.fields]
        fields = ["history_id", "modified", "history_user", "content"]


class NoteSerializer(WritableNestedModelSerializer):
    history = HisoricalNoteSerializer(read_only=True, many=True)
    user = SerializerMethodField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'content', 'modified', 'history', 'user')
        extra_kwargs = {'modified': {'read_only': True}}
        read_only_fields = ("user", )

    def get_user(self, obj):
        from infoauto.users.serializers.users import SimplestUserSerializer
        return SimplestUserSerializer(obj.user).data

    def update(self, instance, validated_data):
        if validated_data.get('content', '') != self.instance.content:
            return super().update(instance, validated_data)
        else:
            return self.instance

    def to_representation(self, instance):
        view = self.context.get('view')
        self.fields.pop('history', None) if view and view.action not in ['retrieve'] else None
        return super().to_representation(instance)
