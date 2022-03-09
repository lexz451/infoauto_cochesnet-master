from django import forms
from django.conf import settings
from django.db.models import Max, Q
from django.utils import formats, timezone
from django_filters import BooleanFilter

from django_filters.rest_framework import FilterSet, DateTimeFilter as BaseDateTimeFilter, DateRangeFilter, CharFilter, \
    NumberFilter

from infoauto.leads.lead_master import LeadMaster
from infoauto.leads.models import Lead, Task
from infoauto.leads.models.lead_management import LeadManagement
from infoauto.leads.models.leads import LeadAction, LeadCalendar


class DateTimeField(forms.DateTimeField):
    input_formats = list(formats.get_format_lazy('DATETIME_INPUT_FORMATS')) + settings.REST_FRAMEWORK['DATETIME_INPUT_FORMATS']


class DateTimeFilter(BaseDateTimeFilter):
    field_class = DateTimeField


class LeadMasterFilter(FilterSet):

    created = DateTimeFilter()
    created_start_date = DateTimeFilter('created', lookup_expr='gt')
    created_end_date = DateTimeFilter('created', lookup_expr='lt')

    class Meta:
        model = LeadMaster
        fields = {
            'user': ['exact']
        }

class LeadFilter(FilterSet):

    created = DateTimeFilter()
    created_start_date = DateTimeFilter('created', lookup_expr='gte')
    created_end_date = DateTimeFilter('created', lookup_expr='lte')

    start = DateTimeFilter('created', lookup_expr='gte')
    end = DateTimeFilter('created', lookup_expr='lte')

    date_start = DateTimeFilter('modified', lookup_expr='gte')
    date_end = DateTimeFilter('modified', lookup_expr='lte')

    kpi_filter = CharFilter(method='kpi_filter_method')

    without_pending_tasks = BooleanFilter(method='without_pending_tasks_method')
    without_pending_trackings = BooleanFilter(method='without_pending_trackings_method')

    without_outgoing_calls = BooleanFilter(method='without_outgoing_calls_method')

    user = NumberFilter('user_id', lookup_expr='exact')

    def without_pending_tasks_method(self, queryset, name, value):
        if value:
            queryset = queryset.filter(~Q(tasks__is_traking_task=False))
        else:
            queryset = queryset.filter(tasks__is_traking_task=False)

        return queryset.distinct()

    def without_pending_trackings_method(self, queryset, name, value):
        if value:
            queryset = queryset.filter(~Q(tasks__is_traking_task=True))
        else:
            queryset = queryset.filter(tasks__is_traking_task=True)

        return queryset.distinct()

    def without_outgoing_calls_method(self, queryset, name, value):
        # queryset = queryset.filter(~Q(lead_managements__event='outcomming_all'))
        if value:
            queryset = queryset.filter(~Q(callcontrolleadmodel__call_control__call_origin='user'))
        else:
            queryset = queryset.filter(callcontrolleadmodel__call_control__call_origin='user')

        return queryset.distinct()

    def kpi_filter_method(self, queryset, name, value):
        if value == 'not_attended':
            queryset = queryset.filter(status='new')
        elif value == 'pending_task':
            queryset = queryset.filter(
                tasks__is_traking_task=False,
                tasks__realization_date_check=False,
                tasks__planified_realization_date__gte=timezone.now())
        elif value == 'delayed_task':
            queryset = queryset.filter(
                tasks__is_traking_task=False,
                tasks__realization_date_check=False,
                tasks__planified_realization_date__lt=timezone.now())
        elif value == 'pending_tracking':
            queryset = queryset.filter(
                tasks__is_traking_task=True,
                tasks__realization_date_check=False,
                tasks__planified_realization_date__gte=timezone.now())
        elif value == 'delayed_tracking':
            queryset = queryset.filter(
                tasks__is_traking_task=True,
                tasks__realization_date_check=False,
                tasks__planified_realization_date__lt=timezone.now())

        return queryset.distinct()

    class Meta:
        model = Lead
        fields = {
            'user_id': ['in'],
            'status': ['in'],
            'client__phone': ['icontains', 'isnull'],
            'client__email': ['icontains'],
            'client__name': ['icontains'],
            'client__surname': ['icontains'],
            'client__identification': ['icontains'],
            'client__business_name': ['icontains'],
            'client__desk_phone': ['icontains'],
            'client__province_id': ['exact'],
            'client__location_id': ['exact'],
            'tags': ['exact'],
            'tags__content': ['icontains'],
            'concessionaire': ['in'],
            'score': ['exact'],
            'result': ['exact', 'isnull'],
            'result_reason': ['exact'],
            'request_type': ['exact'],
            'source_id': ['in'],
            'source__channel_id': ['in'],
            'source__channel__name': ['in'],
            'source__origin_id': ['in'],
            'vehicles__vehicle_type': ['exact'],
            'vehicles__comercial_category': ['exact'],
            'vehicles__gear_shift': ['exact'],
            'vehicles__gas': ['exact'],
            'vehicles__brand_model': ['in'],
            'vehicles__model': ['icontains'],
            'vehicles__version': ['icontains'],
            'tasks__author_id': ['exact'],
            'tasks__type': ['in'],
            'tasks__subtype': ['in'],
            'tasks__media': ['in'],
            'tasks__is_traking_task': ['exact'],
            'tasks__is_click2call': ['exact'],
            'tasks__realization_date_check': ['exact'],
            'tasks__realization_date': ['gt', 'lt', 'isnull'],
            'tasks__planified_realization_date': ['gt', 'lt'],
            'tasks__tracking_date_check': ['exact'],
            'lead_managements__event': ['exact'],
        }


class LeadManagementFilter(FilterSet):

    created_start_date = DateTimeFilter('created', lookup_expr='gte')
    created_end_date = DateTimeFilter('created', lookup_expr='lte')

    class Meta:
        model = LeadManagement
        fields = {'lead': ['exact'], 'user': ['exact']}


class LeadActionDateTimeFilter(DateTimeFilter):
    def filter(self, qs, value):
        if value:
            lookup = '%s__%s__%s' % (self.field_name, 'max', self.lookup_expr)
            qs = qs.annotate(Max(self.field_name)).filter(**{lookup: value}).distinct()
        return qs


class LeadColsFilter(FilterSet):
    id_excluded = NumberFilter(field_name='id', exclude=True)
    lead_task_date_start = DateTimeFilter('lead_task_date', lookup_expr='gte')
    lead_task_date_end = DateTimeFilter('lead_task_date', lookup_expr='lte')
    last_action_start_date = LeadActionDateTimeFilter('leadaction__date', lookup_expr='gte')
    last_action_end_date = LeadActionDateTimeFilter('leadaction__date', lookup_expr='lte')

    date_start = DateTimeFilter('modified', lookup_expr='gte')
    date_end = DateTimeFilter('modified', lookup_expr='lte')

    created_start_date = DateTimeFilter('created', lookup_expr='gte')
    created_end_date = DateTimeFilter('created', lookup_expr='lte')

    class Meta:
        model = Lead
        fields = {
            'request__task__type': ['exact'],
            'user_id': ['in'],
            'status': ['exact'],
            'client__phone': ['icontains'],
            'client__email': ['icontains'],
            'client__name': ['icontains'],
            'client__surname': ['icontains'],
            'client__identification': ['icontains'],
            'client__business_name': ['icontains'],
            'client__desk_phone': ['icontains'],
            'client__province_id': ['exact'],
            'client__location_id': ['exact'],
            'tags': ['exact'],
            'tags__content': ['icontains'],
            'concessionaire': ['in'],
            'score': ['exact'],
            'result': ['exact'],
            'result_reason': ['exact'],
            'request_type': ['exact'],
            'source_id': ['in'],
            'source__channel_id': ['in'],
            'source__origin_id': ['in'],
            'vehicles__vehicle_type': ['exact'],
            'vehicles__comercial_category': ['exact'],
            'vehicles__gear_shift': ['exact'],
            'vehicles__gas': ['exact'],
            'vehicles__brand_model': ['in'],
            'vehicles__model': ['icontains'],
            'vehicles__version': ['icontains'],
            'tasks__author_id': ['exact'],
            'tasks__type': ['in'],
            'tasks__subtype': ['in'],
            'tasks__media': ['in'],
            'tasks__is_traking_task': ['exact'],
            'tasks__is_click2call': ['exact'],
            'tasks__realization_date_check': ['exact'],
            'tasks__realization_date': ['gt', 'lt'],
            'tasks__planified_realization_date': ['gt', 'lt'],
            'tasks__tracking_date_check': ['exact'],
        }


class LeadActionFilter(FilterSet):
    date_start = DateTimeFilter('date', lookup_expr='gte')
    date_end = DateTimeFilter('date', lookup_expr='lte')
    start = DateTimeFilter('date', lookup_expr='gte')
    end = DateTimeFilter('date', lookup_expr='lte')

    class Meta:
        model = LeadAction
        fields = {'lead': ['exact'], 'user': ['exact']}


class LeadCalendarFilter(FilterSet):
    date_start = DateTimeFilter('date', lookup_expr='gte')
    date_end = DateTimeFilter('date', lookup_expr='lte')
    start = DateTimeFilter('date', lookup_expr='gte')
    end = DateTimeFilter('date', lookup_expr='lte')
    result = CharFilter('result', lookup_expr='exact')

    kpi_filter = CharFilter(method='kpi_filter_method')

    def kpi_filter_method(self, queryset, name, value):
        if value == 'not_attended':
            queryset = queryset.filter(type='pending_lead')
        elif value == 'pending_task':
            queryset = queryset.filter(type='pending_task', date__gte=timezone.now())
        elif value == 'delayed_task':
            queryset = queryset.filter(type='pending_task', date__lt=timezone.now())
        elif value == 'pending_tracking':
            queryset = queryset.filter(type='pending_traking', date__gte=timezone.now())
        elif value == 'delayed_tracking':
            queryset = queryset.filter(type='pending_traking', date__lt=timezone.now())

        return queryset

    class Meta:
        model = LeadCalendar
        fields = {'lead': ['exact'], 'user': ['exact'], 'status': ['in'], 'result': ['in']}
        #fields = {'id': ['exact'], 'user': ['exact']}


class TaskFilter(FilterSet):
    date_start = DateTimeFilter('realization_date', lookup_expr='gte')
    date_end = DateTimeFilter('realization_date', lookup_expr='lte')
    start = DateTimeFilter('realization_date', lookup_expr='gte')
    end = DateTimeFilter('realization_date', lookup_expr='lte')

    user = NumberFilter('author_id', lookup_expr='exact')

    class Meta:
        model = Task
        fields = {'lead': ['exact']}

