# -*- coding: utf-8 -*-

from django.db.models import CharField, ManyToManyField
from django.db.models import FileField
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from infoauto.source_channels.models import Channel


class Origin(TimeStampedModel):
    name = CharField(max_length=255)
    icon = FileField()
    available_channels = ManyToManyField(Channel, blank=True)

    class Meta:
        verbose_name = _("Origin")
        verbose_name_plural = _("Origins")
