from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json


class NetelipConsumer(WebsocketConsumer):
    mask = None
    room_group_name = None

    @staticmethod
    def check_permissions(user, mask):
        """
        if (not user.is_authenticated) or (str(user.pk) != str()):
            return False
        """
        return True

    def connect(self):
        self.mask = self.scope['url_route']['kwargs']['mask']  # Can be phone number or literal "admin"
        if not self.check_permissions(user=self.scope['user'], mask=self.mask):
            return self.close()
        self.room_group_name = 'received_call_%s' % self.mask

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive received_call from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        received_call = text_data_json['received_call']

        # Send received_call to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'received_call',
                'received_call': received_call
            }
        )

    # Receive received_call from room group
    def received_call(self, event):
        received_call = event['received_call']
        # Send received_call to WebSocket
        self.send(text_data=json.dumps({
            'received_call': received_call
        }))
