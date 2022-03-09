from drf_writable_nested import WritableNestedModelSerializer
from slugify import slugify

from infoauto.source_channels.models import Channel


class ChannelSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'slug', 'name')
        read_only_fields = ("slug", )

    def validate(self, attrs):
        if attrs.get('name'):
            attrs['slug'] = slugify(attrs['name'])
        return super().validate(attrs)
