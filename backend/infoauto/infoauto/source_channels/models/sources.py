# -*- coding: utf-8 -*-

from django.db.models import CharField, ForeignKey, CASCADE, Manager
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from infoauto.common.util_phone import normalize_phone
from infoauto.leads.models.origins import Origin
from infoauto.leads.models.concessionaires import Concessionaire
from infoauto.source_channels.models.channels import Channel
from rest_framework.fields import SerializerMethodField


class SourceManager(Manager):
    def get_safe(self, *args, **kwargs):
        try:
            instance = super().get_queryset().get(**kwargs)
        except self.model.DoesNotExist:
            instance = None
        return instance


class Source(TimeStampedModel):
    channel = ForeignKey(Channel, on_delete=CASCADE, related_name="source_channel")
    data = CharField(max_length=255, blank=True, null=True)
    origin = ForeignKey(Origin, on_delete=CASCADE)
    concession = ForeignKey(Concessionaire, on_delete=CASCADE)
    objects = SourceManager()

    @property
    def concession_name(self):
        return self.concession.name

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")
        unique_together = ('channel', 'data', 'origin', 'concession')

    def __str__(self):
        return "%s %s %s %s" % (self.channel.slug, self.data, self.origin.name, self.concession.name)

    def save(self, *args, **kwargs):

        if self.channel.slug == 'phone':
            self.data = normalize_phone(self.data)

        super().save(*args, **kwargs)
