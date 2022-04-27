# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import ManyToManyField, TextField, CharField, ForeignKey, EmailField, FloatField, BooleanField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from infoauto.common.util_phone import normalize_phone
from infoauto.leads.models.notes import Note
from infoauto.leads.models.common import phone_regex
from infoauto.users.admin import User
from infoauto.work_calendar.models import Week


class Phone(TimeStampedModel):
    number = CharField(validators=[phone_regex], max_length=17, help_text=_("Phone"), unique=True)
    description = TextField(blank=True, null=True)
    origin = ForeignKey("Origin", blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")

    def save(self, *args, **kwargs):

        self.number = normalize_phone(self.number)
        super().save(*args, **kwargs)


class Email(TimeStampedModel):
    email = EmailField(unique=True)
    description = TextField(blank=True, null=True)
    origin = ForeignKey("Origin", blank=True, null=True, on_delete=models.PROTECT)


class Concessionaire(TimeStampedModel):
    name = CharField(max_length=255)
    phones = ManyToManyField(Phone)
    emails = ManyToManyField(Email, blank=True)
    address = TextField(blank=True, null=True)
    latitude = FloatField(blank=True, null=True)
    longitude = FloatField(blank=True, null=True)
    schedule = TextField(blank=True, null=True)
    web = CharField(max_length=255, blank=True, null=True)
    web_coches_net = CharField(max_length=255, blank=True, null=True)
    date_notes = TextField(blank=True, null=True)
    appraisal_notes = TextField(blank=True, null=True)
    financing_notes = TextField(blank=True, null=True)
    warranty_notes = TextField(blank=True, null=True)
    service_notes = TextField(blank=True, null=True)
    user = ManyToManyField(
        User,
        through='UserConcession',
        through_fields=('concessionaire', 'user'),
        help_text=_("Relación entre concesionario y usuario"), blank=True)
    work_calendar = ForeignKey(Week, on_delete=models.PROTECT, blank=True, null=True)
    notes = ManyToManyField(Note, blank=True)
    mask_c2c = CharField(validators=[phone_regex], max_length=17, blank=True, null=True,
                         verbose_name=_("Mascara [src] a mostrar como llamante"))
    concession_phone = CharField(validators=[phone_regex], max_length=17, blank=True, null=True,
                                 verbose_name=_("Número de la casa oficial de la concesión"))
    hubspot_api_key = CharField(max_length=64, blank=True, null=True, verbose_name=_("Api Key para HubSpot"))
    hubspot_id = CharField(max_length=64, blank=True, null=True, verbose_name=_("ID de concesionario en HubSpot"))

    class Meta:
        verbose_name = _("Concessionaire")
        verbose_name_plural = _("Concessionaires")
        unique_together = ("id", "work_calendar")

    def save(self, *args, **kwargs):

        self.concession_phone = normalize_phone(self.concession_phone)
        self.mask_c2c = normalize_phone(self.mask_c2c)
        super().save(*args, **kwargs)


class UserConcession(TimeStampedModel):
    concessionaire = ForeignKey(Concessionaire, on_delete=models.CASCADE, related_name='userconcession')
    user = ForeignKey(User, on_delete=models.CASCADE)
    is_concessionaire_admin = BooleanField(default=False, help_text=_("Administrador del concesionario"))
    is_business_manager = BooleanField(default=False, help_text=_("Gestor del concesionario"))

    class Meta:
        verbose_name = _("Relación Usuario Concesionario")
        verbose_name_plural = _("Relaciones usuario concessionario")
