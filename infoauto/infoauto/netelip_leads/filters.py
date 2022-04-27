# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from django_filters import BooleanFilter

from infoauto.netelip.filters import CallControlFilter as BaseCallControlFilter


class CallControlFilter(BaseCallControlFilter):
    call_without_lead = BooleanFilter('callcontrolleadmodel__lead', lookup_expr='isnull',
                                      help_text=_("1=All, 2=True, 3=False"))

    class Meta(BaseCallControlFilter.Meta):
        new_fields = {"call_origin": ["exact"],}
        fields = {**BaseCallControlFilter.Meta.fields, **new_fields}
