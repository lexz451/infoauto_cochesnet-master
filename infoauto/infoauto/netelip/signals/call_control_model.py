# -*- coding: utf-8 -*-

import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from infoauto.common.encoders import DecimalEncoder
from infoauto.netelip.models import CallControlModel
from infoauto.netelip.serializers import CallControlSerializer


@receiver(post_save, sender=CallControlModel)
def web_socket_received_call(sender, instance, created, *args, **kwargs):
    if (created or instance.command == 'dial') and instance.typesrc == 'did':
        # Enviamos que hay un mensaje nuevo
        channel_layer = get_channel_layer()
        # Send message to room group
        serializer_class = getattr(instance, 'serializer_class', CallControlSerializer)
        notification = serializer_class(instance=instance).data
        if getattr(instance, 'extra_data', None):
            notification = {**notification, **instance.extra_data}
        async_to_sync(channel_layer.group_send)(
            "received_call_%s" % instance.dst.replace('+', ''),
            {
                'type': 'received_call',
                'received_call': json.dumps(notification, cls=DecimalEncoder)
            }
        )
        async_to_sync(channel_layer.group_send)(
            "received_call_admin",
            {
                'type': 'received_call',
                'received_call': json.dumps(notification, cls=DecimalEncoder)
            }
        )
