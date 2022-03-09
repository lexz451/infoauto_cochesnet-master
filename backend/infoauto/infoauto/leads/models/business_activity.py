# -*- coding: utf-8 -*-

from model_utils.models import TimeStampedModel
from django.db.models import CharField, ForeignKey, PositiveIntegerField, PROTECT


class Sector(TimeStampedModel):
	custom_id = CharField(max_length=4, null=True)
	name = CharField(max_length=256, null=True)


class BusinessActivity(TimeStampedModel):
	custom_id = PositiveIntegerField(null=True)
	activity = CharField(max_length=256, null=True)
	sector = ForeignKey(Sector, on_delete=PROTECT)

