from model_utils.models import TimeStampedModel
from django.db.models import Model, ForeignKey, CASCADE, TextField, CharField

COMMENT_ORIGINS = [
    ("whatsapp", "Whatsapp"),
    ("other", "Otro"),
]

COMMENT_EVENT = [
    ("templateMessageSent", "TemplateMessageSent"),
    ('message', 'Message')
]

class Comment(TimeStampedModel):
    #lead = ForeignKey(Lead, on_delete=CASCADE)
    text = TextField(name='text', blank=True)
    origin = CharField(name='origin', choices=COMMENT_ORIGINS, max_length=100,  blank=True)
    timestamp = CharField(name='timestamp', max_length=250,  blank=True)
    contact_name = CharField(name='contact_name', max_length=255, blank=True)
    event_type = CharField(name='event_type', choices=COMMENT_EVENT, max_length=100,  blank=True)
    wa_id = CharField(name='wa_id', max_length=255,  blank=True)