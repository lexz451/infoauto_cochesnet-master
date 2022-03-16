from distutils.text_file import TextFile
from django.db.models import Model, TextField, CharField, DateField, DateTimeField, EmailField, ManyToManyField, BooleanField, ForeignKey, IntegerField, PROTECT, SET_NULL, CASCADE
from infoauto.source_channels.models import Source, Channel
from infoauto.users.models import User, EVENT_LEAD_NOT_ATTENDED_KEY
from infoauto.leads.models import Concessionaire, Origin, Note
from model_utils.models import TimeStampedModel

CAMPAIGN_TYPES = [
]

CAMPAIGN_STATUS = []

class Expense(Model):
    amount = IntegerField()
    date = DateField()

class Campaign(TimeStampedModel):
    name = CharField(max_length=255, null=True, blank=True)
    RSPCRM_campaingId = CharField(max_length=255, null=True, blank=True)
    RSPCRM_origin = CharField(max_length=255, null=True, blank=True)
    campaignType = CharField(max_length=255,choices=CAMPAIGN_TYPES, null=True)
    brandRange = CharField(max_length=255, null=True, blank=True)
    distributionBranch = CharField(max_length=255, null=True, blank=True)
    startDate = DateTimeField(default=None, null=True)
    endDate = DateTimeField(default=None, null=True)
    isActive = BooleanField(default=False)
    key = CharField(max_length=255, null=True, blank=True)
    goal = CharField(max_length=255, null=True, blank=True)
    concessionaire = ForeignKey(Concessionaire, null=True, on_delete=SET_NULL)
    productName = CharField(max_length=255, null=True, blank=True)
    sourceSystem = CharField(max_length=255, null=True, blank=True)
    status = CharField(max_length=255,choices=CAMPAIGN_STATUS, null=True)
    offer = IntegerField(default=0)
    url = CharField(max_length=255, null=True, blank=True)
    communicationType = CharField(max_length=255, null=True, blank=True)
    legalEntityPartnerNumber = CharField(max_length=255, null=True, blank=True)
    origin = ForeignKey(Origin, null=True, on_delete=SET_NULL)
    source = ForeignKey(Source, null=True, on_delete=SET_NULL)
    model = CharField(max_length=255, blank=True, null=True)
    version = CharField(max_length=255, blank=True, null=True)
    investment = IntegerField(default=0)
    #user = ForeignKey(User, on_delete=CASCADE)
    utm_campaing = CharField(max_length=255, blank=True, null=True)
    utm_source = CharField(max_length=255, blank=True, null=True)
    utm_content = CharField(max_length=255, blank=True, null=True)
    note = ManyToManyField(Note, blank=True)
    expenses = TextField(default="[]")





