# -*- coding: utf-8 -*-
import calendar
import datetime

import pytz
from django.conf import settings
from django.db.models import Q

from infoauto.leads.models import Concessionaire
from django.utils import six, timezone
from rest_framework.compat import (InvalidTimeError)
from django.utils.timezone import utc

def default_timezone():
    return timezone.get_current_timezone() if settings.USE_TZ else None

def enforce_timezone(my_datetime):

    field_timezone = default_timezone()
    if field_timezone is not None:
        if timezone.is_aware(my_datetime):
            try:
                return my_datetime.astimezone(field_timezone)
            except OverflowError:
                raise Exception('overflow')
        try:
            return timezone.make_aware(my_datetime, field_timezone)
        except InvalidTimeError:
            raise Exception('make_aware')

    elif (field_timezone is None) and timezone.is_aware(my_datetime):
        return timezone.make_naive(my_datetime, utc)
    return my_datetime


def special_date_ranges(date_range):
    query = {}
    if date_range == 'today':
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min,
                                              tzinfo=pytz.timezone(settings.TIME_ZONE))
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max,
                                              tzinfo=pytz.timezone(settings.TIME_ZONE))
        query = {'lead_task_date__range': (today_min, today_max)}
    elif date_range == 'yesterday':
        today_min = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(1),
                                              datetime.time.min,
                                              tzinfo=pytz.timezone(settings.TIME_ZONE))
        today_max = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(1),
                                              datetime.time.max,
                                              tzinfo=pytz.timezone(settings.TIME_ZONE))
        query = {'lead_task_date__range': (today_min, today_max)}
    elif date_range == 'week':
        d = datetime.date.today()
        if d.weekday() != 6:
            while d.weekday() != 6:
                d += datetime.timedelta(1)
        sunday = datetime.datetime.combine(d, datetime.time.max,
                                           tzinfo=pytz.timezone(settings.TIME_ZONE))
        d = datetime.date.today()
        if d.weekday() != 0:
            while d.weekday() != 0:
                d -= datetime.timedelta(1)
        monday = datetime.datetime.combine(d, datetime.time.min,
                                           tzinfo=pytz.timezone(settings.TIME_ZONE))
        query = {'lead_task_date__range': (monday, sunday)}
    elif date_range == 'month':
        first = datetime.datetime.combine(datetime.date.today().replace(day=1),
                                          datetime.time.min,
                                          tzinfo=pytz.timezone(settings.TIME_ZONE))
        today = datetime.date.today()
        last_day = calendar.monthrange(month=today.month, year=today.year)[1]
        last = datetime.datetime.combine(datetime.date.today().replace(day=last_day),
                                         datetime.time.max,
                                         tzinfo=pytz.timezone(settings.TIME_ZONE))
        query = {'lead_task_date__range': (first, last)}
    else:
        pass
    return query


def is_license_plate(data):
    """
    Check if plate number is spanish license plate
    :param data:
    :return: (data|False)
    """
    '''
    import re

    if not data:
        return data
    data = data.upper()
    data = "".join(data.split())
    pattern = re.compile(r"\d{4}[A-Z]{3}")
    res = pattern.match(data)
    if res and res[0] == data:
        return data
    return False
    '''
    return data


def set_status_finish_date(instance, save_instance=None):
    """
    Update Tasks when Lead finish and set finish_date to now and status to 'end'
    :param instance: Lead instance
    :param save_instance: If True, Lead instance sa
    :return: Lead instance
    """
    date_now = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    for i in instance.request.task.all():
        changes = False
        if not i.realization_date_check:
            changes = True
            i.realization_date_check = True
            i.realization_date = date_now
        if i.planified_tracking_date and not i.tracking_date_check:
            changes = True
            i.tracking_date_check = True
            i.realization_date = date_now
        i.save() if changes else None
    instance.finish_date = date_now
    instance.status = 'end'
    instance.save() if save_instance else None
    return instance


def update_status(lead, force_status=False):
    """
    Set status
    :param lead: Lead instance
    :param force_status: Set status recived on instance. Not automatic status.
    :return: (tracing|commercial_management)
    """
    status = lead.status
    if lead.status != 'end' and not force_status:
        queryset = lead.request.task.all()
        if queryset.exists():
            if queryset.filter(realization_date_check=True).exists():
                status = 'tracing'
            elif queryset.filter(planified_realization_date__isnull=False, realization_date_check=False).exists():
                status = 'commercial_management'
            else:
                status = 'tracing'
    return status


def popattr(obj, name, default=None):
    try:
        data = getattr(obj, name, default)
        delattr(obj, name)
        return data
    except AttributeError:
        return default


def get_concession_instance(email=None, phone=None):
    instance = None
    if phone or email:
        query_params = Q()
        phone = phone[2:] if phone and phone.startswith('+') else phone
        if phone:
            query_params = Q(phones__number__icontains=phone)
        if email:
            query_params = query_params | Q(emails__email=email)
        try:
            instance = Concessionaire.objects.get(query_params)
        except Concessionaire.DoesNotExist:
            pass
    return instance

def create_excel_template(serializer, workbook, worksheet):

    columns = [k for k, v in serializer.get_fields().items() if not v.write_only]
    for i, col in enumerate(columns):
        add_column_to_excel(col, workbook, worksheet, i)

    add_column_to_excel("imported_lead_id", workbook, worksheet, len(columns))
    add_column_to_excel("imported_result", workbook, worksheet, len(columns) + 1)
    add_column_to_excel("imported_error", workbook, worksheet, len(columns) + 2)


def add_column_to_excel(content, workbook, worksheet, position):
    bold_format = worksheet.add_format({'bold': True, 'bg_color': "#d8d8d8", })
    workbook.write(0, position, content, bold_format)
    workbook.set_column(0, position, len(content) * 2.5)

def add_value_to_excel(content, workbook, position_x, position_y):
    workbook.write(position_x, position_y, content)


def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj

def get_column_cell(obj, name):
    try:
        attr = multi_getattr(obj, name)
    except ObjectDoesNotExist:
        return None
    if hasattr(attr, '_meta'):
        # A Django Model (related object)
        return str(attr).strip()
    elif hasattr(attr, 'all'):
        # A Django queryset (ManyRelatedManager)
        return ', '.join(str(x).strip() for x in attr.all())