# -*- coding: utf-8 -*-

import datetime
from numbers import Integral
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from infoauto.common.simple_history import HistoricalRecords
from django.db.models import (
    CharField,
    IntegerField,
    ForeignKey,
    BooleanField,
    PROTECT,
    TextField,
    SET_NULL,
    CASCADE,
    DateTimeField,
    URLField
)


class HistoricalRecordsVehicle(HistoricalRecords):
    def post_save(self, instance, created, **kwargs):
        msg = None
        changed_fields = self.get_changed_fields(sender=kwargs['sender'], instance=instance)
        if created:
            msg = "El vehículo ha sido dado de alta en el sistema"
        elif changed_fields:
            msg = "El vehículo ha sido modificado"
        return super().post_save(instance=instance, created=created, changeReason=msg, **kwargs)


class GasType(TimeStampedModel):
    name = CharField(max_length=255)


def year_choices():
    return [(r, r) for r in range(1900, datetime.date.today().year+1)]


VEHICLE_TYPE_CHOICES = [
    ("new", _("Nuevo")),
    ("km0", _("Km0")),
    ("seminew", _("Seminuevo")),
    ("used", _("Ocasión")),
]

COMERCIAL_CATEGORY_CHOICES = [
    ("request_product", _("Producto solicitado")),
    ("offered_product", _("Producto ofertado"))
]

GEAR_SHIFT_CHOICES = [
    ("manual", _("Manual")),
    ("auto", _("Auto"))
]

VEHICLE_SEGMENT_CHOISES = [
    ("tur", _("Turismo")),
    ("comercial", _("Comercial")),
    ("moto", _("Motocicleta")),
    ("other", _("Otro"))
]

VEHICLE_PURCHASE_CHOISES = [
    ("count", _("CONTADO")),
    ("rent", _("RENTING")),
    ("lease", _("LEASING")),
    ("fin", _("FINANCIACION"))
]

FINANCIAL_TERMS_CHOISES = [
    (3, _("3")),
    (6, _("6")),
    (9, _("9")),
    (12, _("12")),
    (15, _("15")),
    (18, _("18")),
    (21, _("21")),
    (24, _("24")),
    (27, _("27")),
    (30, _("30")),
    (33, _("33")),
    (36, _("36")),
    (39, _("39")),
    (42, _("42")),
    (45, _("45")),
    (48, _("48")),
    (51, _("51")),
    (54, _("54")),
    (57, _("57")),
    (60, _("60")),
    (63, _("63")),
    (66, _("66")),
    (69, _("69")),
    (72, _("72")),
    (75, _("75")),
    (78, _("78")),
    (81, _("81")),
    (84, _("84")),
    (87, _("87")),
    (90, _("90")),
    (93, _("93")),
    (96, _("96")),
    (99, _("99")),
    (102, _("102")),
    (105, _("105")),
    (108, _("108")),
    (111, _("111")),
    (114, _("114")),
    (117, _("117")),
    (120, _("120")),
]

OPPORTUNITY_STAGE_CHOISES = [
    (0, _("LOST")),
    (1, _("WON"))
]

REJECTION_CHOISES = [
    ("too_high", _("Price too high")),
    ("other_dealer", _("Has opted for another dealer")),
    ("other_brand", _("Has opted for another brand")),
    ("offer_too_low", _("Trade-in offer too low")),
    ("moved", _("Moved purchase")),
    ("cancel", _("Contract cancelled")),
    ("declined", _("Declined financing")),
    ("used", _("Used vehicle")),
    ("no_news", _("No news from client/prospect")),
    ("lost", _("Lost-Mass Ops"))
]

class Vehicle(TimeStampedModel):
    lead = ForeignKey('Lead', on_delete=CASCADE, related_name='vehicles', blank=True, null=True)

    vehicle_type = CharField(max_length=255, blank=True, null=True, choices=VEHICLE_TYPE_CHOICES)
    comercial_category = CharField(max_length=255, blank=True, null=True, choices=COMERCIAL_CATEGORY_CHOICES)
    power = CharField(max_length=255, blank=True, null=True)
    gear_shift = CharField(max_length=255, blank=True, null=True, choices=GEAR_SHIFT_CHOICES)
    ad_link = CharField(blank=True, null=True, max_length=1024)

    brand_model = CharField(max_length=255, blank=True, null=True)
    model = CharField(max_length=255, blank=True, null=True)
    version = CharField(max_length=255, blank=True, null=True)
    price = CharField(max_length=255, blank=True, null=True)
    km = CharField(max_length=255, blank=True, null=True)
    year = IntegerField(blank=True, null=True, choices=year_choices())
    gas = ForeignKey(GasType, blank=True, null=True, on_delete=PROTECT)
    sold = BooleanField(default=False)
    history = HistoricalRecordsVehicle()
    origin = ForeignKey('Origin', on_delete=SET_NULL, blank=True, null=True, related_name='vehicles')
    media = ForeignKey('source_channels.Channel', on_delete=SET_NULL, blank=True, null=True, related_name='vehicles')
    note = TextField(blank=True, null=True)

    number_vehicles = IntegerField(default=0)
    segment = CharField(choices=VEHICLE_SEGMENT_CHOISES, default="other", max_length=100)
    purchase_method = CharField(choices=VEHICLE_PURCHASE_CHOISES, default="count", max_length=100)
    purchase_description = TextField(default="", null=True, blank=True)
    initial_payment = IntegerField(null=True)
    financial_term = IntegerField(choices=FINANCIAL_TERMS_CHOISES, null=True)
    finalcial_km_year = IntegerField(null=True)
    maximum_monthlyfee = IntegerField(null=True)
    pff = IntegerField(null=True)
    percent_comision = IntegerField(null=True)
    total_commision = IntegerField(null=True)
    oportunity_state = IntegerField(choices=OPPORTUNITY_STAGE_CHOISES, null=True)
    rejection_reason = CharField(choices=REJECTION_CHOISES, null=True, max_length=250)
    price_discount = IntegerField(null=True)

    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def __str__(self):
        if self.brand_model and self.model and self.version:
            return "%s %s %s" % (self.brand_model, self.model, self.version)
        if self.brand_model and self.model:
            return "%s %s" % (self.brand_model, self.model)
        if self.brand_model:
            return "%s" % (self.brand_model)
        return ''


ORIGIN = [
    ('national', _('National')),
    ('foreign', _('Foreign'))
]


class Appraisal(TimeStampedModel):
    lead = ForeignKey('Lead', on_delete=CASCADE, related_name='appraisals', blank=True, null=True)

    brand = CharField(max_length=255, blank=True, null=True)
    model = CharField(max_length=255, blank=True, null=True)
    version = CharField(max_length=255, blank=True, null=True)

    km = CharField(max_length=255, blank=True, null=True)
    status = CharField(max_length=255, blank=True, null=True)
    features = CharField(max_length=255, blank=True, null=True)
    circulation_date = DateTimeField(blank=True, null=True)
    evaluation_vo_price = IntegerField(blank=True, null=True)
    total_vehicles = IntegerField(blank=True, null=True)
    total_comercial_vehicles = IntegerField(blank=True, null=True)
    total_tourism_vehicles = IntegerField(blank=True, null=True)
    fleet_notes = TextField(blank=True, null=True)
    license_plate = CharField(max_length=255, blank=True, null=True)

    buy_date = DateTimeField(blank=True, null=True)
    registration_date = DateTimeField(blank=True, null=True)
    last_mechanic_date = DateTimeField(blank=True, null=True)
    cv = IntegerField(blank=True, null=True)
    is_finance = BooleanField(default=False)

    origin = CharField(choices=ORIGIN, max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Appraisal")
        verbose_name_plural = _("Appraisals")


GEARBOX_CHOICES = [
    ('manual', _('Manual')),
    # temp fix
    ('MANUAL', _('Manual')),
    ('automatic', _('Automatico')),
    ('AUTOMATIC', _('Automatico')),
    ('AUTOMATICO', _('Automatico'))
]


class VehicleVersion(TimeStampedModel):

    size = CharField(max_length=32, null=True, blank=True)
    version_name = CharField(max_length=64)
    motor = CharField(max_length=64)
    engine_power = IntegerField()
    fuel = CharField(max_length=255)
    gearbox = CharField(max_length=64, choices=GEARBOX_CHOICES)
    comments = CharField(max_length=128, null=True, blank=True)
    vehicle_model = ForeignKey('VehicleModel', related_name="vehicle_model", on_delete=CASCADE)
    gas_type = ForeignKey('GasType', on_delete=PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _("Vehicle Version")
        verbose_name_plural = _("Vehicle Versions")


class VehicleBrand(TimeStampedModel):

    name = CharField(max_length=64)


class VehicleModel(TimeStampedModel):

    model_name = CharField(max_length=64)
    brand = ForeignKey(VehicleBrand, related_name="vehicle_brand", on_delete=CASCADE)
