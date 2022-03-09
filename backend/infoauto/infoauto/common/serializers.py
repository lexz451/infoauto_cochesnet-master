import base64

import six
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64FileField(serializers.FileField):
    def __init__(self, header='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = header

    def to_internal_value(self, data):
        if isinstance(data, six.string_types) and data.startswith(self.header):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
