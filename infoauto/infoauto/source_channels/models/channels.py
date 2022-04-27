# -*- coding: utf-8 -*-

from django.db.models import SlugField, CharField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Channel(TimeStampedModel):
    slug = SlugField(unique=False)
    name = CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")

    def __str__(self):
        return u"%s (%s)" % (self.name, self.slug)
