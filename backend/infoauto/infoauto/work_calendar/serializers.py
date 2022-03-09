import datetime

import pytz
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from .models import Weekday, Week, WEEKDAY_ATTRS_CHOICES


class WeekdaySerializer(WritableNestedModelSerializer):

    class Meta:
        model = Weekday
        fields = ('id', 'start_hour', 'end_hour', 'working_day')
        extra_kwargs = {'working_day': {'required': True}}

    def validate_start_end_hours(self, attrs):
        start_hour = attrs.get('start_hour', None) or getattr(self.instance, 'start_hour', None)
        end_hour = attrs.get('end_hour', None) or getattr(self.instance, 'end_hour', None)
        if start_hour and end_hour and (start_hour > end_hour):
            raise ValidationError({
                'start_hour': _("Start hour can't be grater than end hour"),
                'end_hour': _("End hour can't be lower than start hour")
            })

    def validate(self, attrs):
        working_day = attrs.get('working_day', None)
        if working_day:
            if not(attrs.get('start_hour') and attrs.get('end_hour')):
                if (not self.instance) or (self.instance and not self.instance.working_day):
                    errors = {i: _("This field is required")
                              for i in ['start_hour', 'end_hour']
                              if i not in attrs.keys()}
                    raise ValidationError(errors)
        elif working_day is False:
            attrs['start_hour'] = None
            attrs['end_hour'] = None
        elif working_day is None and self.instance and self.instance.working_day:
            errors = {}
            if 'start_hour' in attrs.keys() and not attrs['start_hour']:
                errors.update({'start_hour': _("This field is required")})
            if 'end_hour' in attrs.keys() and not attrs['end_hour']:
                errors.update({'end_hour': _("This field is required")})
            if errors:
                raise ValidationError(errors)
        elif not self.instance and working_day is None:
            raise ValidationError({'working_day': _("This field is required")})
        self.validate_start_end_hours(attrs)
        return super().validate(attrs)


class WeekSerializer(WritableNestedModelSerializer):
    monday = WeekdaySerializer(required=True, allow_null=False)
    tuesday = WeekdaySerializer(required=True, allow_null=False)
    wednesday = WeekdaySerializer(required=True, allow_null=False)
    thursday = WeekdaySerializer(required=True, allow_null=False)
    friday = WeekdaySerializer(required=True, allow_null=False)
    saturday = WeekdaySerializer(required=True, allow_null=False)
    sunday = WeekdaySerializer(required=True, allow_null=False)
    open_now = SerializerMethodField(read_only=True)

    class Meta:
        model = Week
        fields = ('id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'open_now')
        required_fields = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    def validate(self, attrs):
        if not self.instance and set(attrs.keys()) != set(self.Meta.required_fields):
            raise ValidationError({i: _("This field is required")
                                   for i in self.Meta.required_fields if i not in attrs.keys()})
        return super().validate(attrs)

    def get_open_now(self, obj):
        now = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        attr = dict(WEEKDAY_ATTRS_CHOICES).get(now.today().weekday()+1)
        weekday = getattr(obj, attr, None) if attr else None
        if weekday and weekday.start_hour and weekday.end_hour:
            return weekday.start_hour <= now.time() <= weekday.end_hour
        return False
