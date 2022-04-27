from django.apps import apps

from drf_writable_nested import WritableNestedModelSerializer

from infoauto.tags_app.models import Tag


class HisoricalTagSerializer(WritableNestedModelSerializer):
    class Meta:
        model = apps.get_model('tags_app', model_name='HistoricalTag')
        # fields = [i.name for i in HistoricalNote._meta.fields]
        fields = ["history_id", "modified", "history_user", "content"]


class TagSerializer(WritableNestedModelSerializer):
    history = HisoricalTagSerializer(read_only=True, many=True)

    class Meta:
        model = Tag
        fields = ('id', 'content', 'modified', 'history')
        extra_kwargs = {
            'modified': {'read_only': True},
            'content': {'allow_null': True, 'allow_blank': True}
        }

    def update(self, instance, validated_data):
        if validated_data.get('content', '') != self.instance.content:
            return super().update(instance, validated_data)
        else:
            return self.instance
