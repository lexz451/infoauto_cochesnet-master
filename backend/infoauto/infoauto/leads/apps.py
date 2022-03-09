from django.apps import AppConfig
from rest_framework.pagination import PageNumberPagination


class LeadsAppConfig(AppConfig):

    name = "infoauto.leads"
    verbose_name = "Leads"

    def ready(self):
        import infoauto.leads.signals


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def __init__(self):
        super().__init__()
        self.request = None

    def get_page_size(self, request):
        self.request = request
        return super().get_page_size(request)

    def django_paginator_class(self, queryset, page_size):
        if self.request.GET.get('page_size', '') == 'all' and len(queryset) > 0:
            page_size = len(queryset)
        return super().django_paginator_class(queryset, page_size)
