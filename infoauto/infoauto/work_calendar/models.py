from django.db import models
from django.db.models import TimeField, BooleanField, ForeignKey
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

WEEKDAY_CHOICES = (
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
)

WEEKDAY_ATTRS_CHOICES = (
    (1, "monday"),
    (2, "tuesday"),
    (3, "wednesday"),
    (4, "thursday"),
    (5, "friday"),
    (6, "saturday"),
    (7, "sunday"),
)



class Weekday(TimeStampedModel):
    start_hour = TimeField(blank=True, null=True)
    end_hour = TimeField(blank=True, null=True)
    working_day = BooleanField(default=False)

    class Meta:
        verbose_name = _("Weekday")
        verbose_name_plural = _("Weekdays")


class Week(TimeStampedModel):
    monday = ForeignKey(Weekday, on_delete=models.CASCADE, related_name='week_as_monday')
    tuesday = ForeignKey(Weekday, on_delete=models.CASCADE, related_name='week_as_tuesday')
    wednesday = ForeignKey(Weekday, on_delete=models.CASCADE, related_name='week_as_wednesday')
    thursday = ForeignKey(Weekday, on_delete=models.CASCADE, related_name='week_as_thursday')
    friday = ForeignKey(Weekday, on_delete=models.CASCADE, related_name='week_as_friday')
    saturday = ForeignKey(Weekday, on_delete=models.CASCADE, related_name='week_as_saturday')
    sunday = ForeignKey(Weekday, on_delete=models.CASCADE, related_name='week_as_sunday')

    class Meta:
        verbose_name = _("Week")
        verbose_name_plural = _("Weeks")
        unique_together = (('id', 'monday'), ('id', 'tuesday'), ('id', 'wednesday'),
                           ('id', 'thursday'), ('id', 'friday'), ('id', 'saturday'),
                           ('id', 'sunday'))
