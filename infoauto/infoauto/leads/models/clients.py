# -*- coding: utf-8 -*-

from django.db.models import CharField, EmailField, ForeignKey, IntegerField, PROTECT
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from infoauto.common.simple_history import HistoricalRecords
from infoauto.common.util_phone import normalize_phone

from infoauto.countries.models import Province, Locality
from infoauto.leads.models.common import phone_regex, postal_code_regex
from infoauto.leads.models.business_activity import BusinessActivity, Sector



class HistoricalRecordsClient(HistoricalRecords):

    def post_save(self, instance, created, **kwargs):
        msg = None
        if created:
            msg = "El cliente ha sido dado de alta en el sistema"
        if self.get_changed_fields(sender=kwargs['sender'], instance=instance) and not created:
            msg = "El cliente ha sido modificado"
        return super().post_save(instance=instance, created=created, changeReason=msg, **kwargs)

    def post_delete(self, instance, **kwargs):
        msg = "El cliente ha sido borrado del sistema"
        return super().post_delete(instance, changeReason=msg, **kwargs)


CLIENT_TYPE_CHOICES = [
    ("private", _("Particular")),
    ("freelance", _("Autononomo")),
    ("company", _("Empresa")),
]

CLIENT_SEGMENT_CHOISES = [
    ("tur", _("Turismo")),
    ("comercial", _("Comercial")),
    ("moto", _("Motocicleta")),
    ("other", _("Otro"))
]

class Client(TimeStampedModel):
    name = CharField(max_length=255, null=True, blank=True)
    surname = CharField(max_length=255, null=True, blank=True)
    client_type = CharField(max_length=255, choices=CLIENT_TYPE_CHOICES, default="private")
    identification = CharField(max_length=20, null=True, blank=True)
    business_name = CharField(max_length=512, null=True, blank=True)
    business_activity = ForeignKey(BusinessActivity, blank=True, null=True, on_delete=PROTECT)
    sector = ForeignKey(Sector, blank=True, null=True, on_delete=PROTECT)
    position = CharField(max_length=256, null=True)
    phone = CharField(validators=[phone_regex], max_length=17, help_text=_("Phone"), blank=True, null=True)
    desk_phone = CharField(validators=[phone_regex], max_length=17, help_text=_("Phone2"), blank=True, null=True)
    postal_code = CharField(validators=[postal_code_regex], max_length=5, help_text=_("Postal Code"), blank=True, null=True)
    email = EmailField(blank=True, null=True)
    province = ForeignKey(Province, blank=True, null=True, on_delete=PROTECT)
    location = ForeignKey(Locality, blank=True, null=True, on_delete=PROTECT)
    address1 = CharField(max_length=1024, null=True, blank=True)
    address2 = CharField(max_length=1024, null=True, blank=True)

    segment = CharField(choices=CLIENT_SEGMENT_CHOISES, max_length=255, default="other")
    fleet = IntegerField(null=True)
    fleet2 = IntegerField(null=True)

    history = HistoricalRecordsClient()

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    @property
    def user(self):
        try:
            return self.history.filter(history_type='+').first().history_user
        except AttributeError:
            return None

    @property
    def mobile(self):
        phone = self.phone.replace(' ', '')
        if phone.startswith("+") or phone.startswith("6") or phone.startswith("7"):
            return phone


    def get_full_name(self):
        return str(self.name) if self.name else "" + " " + str(self.surname) if self.surname else ""

    def save(self, *args, **kwargs):

        self.phone = normalize_phone(self.phone)
        self.desk_phone = normalize_phone(self.desk_phone)

        super().save(*args, **kwargs)
