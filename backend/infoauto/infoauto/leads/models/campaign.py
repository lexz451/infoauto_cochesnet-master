# -*- coding: utf-8 -*-

from distutils.text_file import TextFile
from django.utils.translation import gettext_lazy as _
from django.db.models import Model, TextField, CharField, DateField, DateTimeField, EmailField, ManyToManyField, BooleanField, ForeignKey, IntegerField, PROTECT, SET_NULL, CASCADE
from infoauto.source_channels.models import Source, Channel
from infoauto.users.models import User, EVENT_LEAD_NOT_ATTENDED_KEY
from infoauto.leads.models import Concessionaire, Origin, Note, VehicleBrand, VehicleModel, VehicleVersion
from model_utils.models import TimeStampedModel

COMMUNICATION_TYPES = [
    ('type1', "Tipo de Comunicación #1"),
    ('type2', "Tipo de Comunicación #2"),
    ('type3', "Tipo de Comunicación #3")
]

CAMPAIGN_TYPES = [
    ('type1', "Tipo de Campaña #1"),
    ('type2', "Tipo de Campaña #2"),
    ('type3', "Tipo de Campaña #3")
]

CAMPAIGN_STATUS = [
    ('on', "Activo"),
    ('off', "Inactivo")
]


class Campaign(TimeStampedModel):

    #lead = ForeignKey('Lead', on_delete=CASCADE, related_name='campaigns', blank=True, null=True)

    name = CharField(max_length=255, null=True, blank=True)
    # type
    campaignType = CharField(max_length=255,choices=CAMPAIGN_TYPES, null=True)
    # status
    status = CharField(max_length=255,choices=CAMPAIGN_STATUS, null=True)
    # communicationType
    communicationType = CharField(max_length=255,choices=COMMUNICATION_TYPES, null=True)
    # startDate
    startDate = DateTimeField(default=None, null=True)
    # endDate
    endDate = DateTimeField(default=None, null=True)
    # concessionary
    concessionaire = ForeignKey(Concessionaire, null=True, on_delete=SET_NULL)
    # origin
    origin = ForeignKey(Origin, null=True, on_delete=SET_NULL)
    # channel
    channel = ForeignKey(Channel, null=True, blank=True, on_delete=SET_NULL, related_name= "campaigns")
    # source
    source = ForeignKey(Source, null=True, on_delete=SET_NULL)
    # brand
    brand = ForeignKey(VehicleBrand, null=True, on_delete=SET_NULL)
    # model
    model = ForeignKey(VehicleModel, null=True, on_delete=SET_NULL)
    # version
    version = ForeignKey(VehicleVersion, null=True, on_delete=SET_NULL)
    # inv.
    investment = IntegerField(null=True)
    # note
    note = TextField(null=True, blank=True)
    # expenses
    expenses = TextField(default="[]")
    # offer
    # offer = IntegerField(default=0)
    offer = CharField(max_length=250, blank=True, null=True)
    # url
    url = TextField(null=True, blank=True)

    # Fields

    # Hidden fields
    RSPCRM_campaingId = CharField(max_length=255, null=True, blank=True)
    RSPCRM_origin = CharField(max_length=255, null=True, blank=True)
    brandRange = CharField(max_length=255, null=True, blank=True)
    distributionBranch = CharField(max_length=255, null=True, blank=True)
    isActive = BooleanField(default=False)
    key = CharField(max_length=255, null=True, blank=True)
    goal = CharField(max_length=255, null=True, blank=True) 
    productName = CharField(max_length=255, null=True, blank=True)
    sourceSystem = CharField(max_length=255, null=True, blank=True)
    legalEntityPartnerNumber = CharField(max_length=255, null=True, blank=True)
    #user = ForeignKey(User, on_delete=CASCADE)
    utm_campaign = CharField(max_length=255, blank=True, null=True)
    utm_source = CharField(max_length=255, blank=True, null=True)
    utm_content = CharField(max_length=255, blank=True, null=True)
    campaingId = CharField(max_length=255, null=True, blank=True)
    