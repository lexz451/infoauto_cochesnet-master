import json

from django.apps import apps
from django.core.exceptions import ValidationError as DjangoValidationError
from django_filters import FilterSet, DateTimeFilter, Filter, ModelChoiceFilter, BooleanFilter
from rest_framework.exceptions import ValidationError

from infoauto.leads.models import Concessionaire


class SessionWithHistoricFilter(FilterSet):
    start_working_from = DateTimeFilter('start_working', lookup_expr='gte')
    start_working_to = DateTimeFilter('start_working', lookup_expr='lte')
    end_working_from = DateTimeFilter('end_working', lookup_expr='gte')
    end_working_to = DateTimeFilter('end_working', lookup_expr='lte')

    class Meta:
        model = apps.get_model('users', model_name='HistoricalSessionWithHistoric')
        fields = {
            'user__id': ['exact']
        }


class OnlineUserFilter(Filter):

    def filter(self, qs, value):
        if value is not None:
            value = json.loads(value)
        if value is None:
            pass
        elif value is True:
            qs = qs.filter(sessionwithhistoric__isnull=False)
        elif value is False:
            qs = qs.filter(sessionwithhistoric__isnull=False)
        else:
            qs = qs.none()
        if value in [True, False]:
            qs = qs.model.objects.filter(id__in=(i.id for i in qs if i.sessionwithhistoric.online == value))
        return qs


class BooleanFilterAux(Filter):
    def filter(self, qs, value):
        try:
            value = json.loads(value) if value else None
        except json.decoder.JSONDecodeError:
            pass
        try:
            return super().filter(qs, value)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)


class UserFilter(FilterSet):
    online = OnlineUserFilter()
    userconcession__concessionaire__id = ModelChoiceFilter('userconcession__concessionaire',
                                                           queryset=Concessionaire.objects.all())
    is_active = BooleanFilterAux('is_active')
    is_superuser = BooleanFilterAux('is_superuser')
    is_staff = BooleanFilterAux('is_staff')
    is_concession_admin = BooleanFilter(method='filter_is_concession_admin')


    def filter_is_concession_admin(self, queryset, name, value,):
        concession_admin_ids = [user.id for user in queryset if user.is_concession_admin]
        if value:
            return queryset.filter(id__in=concession_admin_ids)
        else:
            return queryset.exclude(id__in=concession_admin_ids)

        return queryset

    class Meta:
        fields = {
            'first_name': ['icontains'], 'last_name': ['icontains'], 'email': ['icontains'],
            'phone': ['icontains'], 'userconcession__concessionaire__id': ['exact'], 'is_active': ['exact'], 'is_concession_admin': ['exact']
        }
