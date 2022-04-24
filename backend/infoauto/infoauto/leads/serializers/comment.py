from infoauto.leads.models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'contact_name', 'text', 'timestamp', 'origin', 'wa_id', 'event_type']