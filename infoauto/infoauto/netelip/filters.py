from django_filters import FilterSet

from infoauto.netelip.models import CallControlModel


class CallControlFilter(FilterSet):
    class Meta:
        model = CallControlModel
        fields = {
            "id_call": ["exact"],
            "api": ["icontains"],
            "src": ["icontains"],
            "dst": ["icontains"],
            "startcall": ["exact"],
            "durationcall": ["exact"],
            "durationcallanswered": ["exact"],
            "command": ["icontains"],
            "options": ["icontains"],
            "description": ["icontains"],
            "dtmf": ["icontains"],
            "statuscode": ["exact"],
            "statuscall": ["icontains"],
            "userdata": ["icontains"],
            "typesrc": ["icontains"],
            "usersrc": ["icontains"],
            "call_origin": ["exact"]
        }
