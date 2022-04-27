from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_condition import Or
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from infoauto.common.util_phone import normalize_phone
from infoauto.leads.models import Concessionaire, Lead
from infoauto.leads.models.lead_management import LeadManagement
from infoauto.leads.serializers import TaskSerializer
from infoauto.netelip.models import Flow
from infoauto.netelip.views import CallControlView as BaseCallControlView, CallReceiverView as BaseCallReceiverView
from infoauto.netelip_leads.filters import CallControlFilter
from infoauto.netelip_leads.serializers import CallControlLeadSerializer, CallControlSerializer, Click2CallSerializer
from infoauto.users.models import EVENT_OUTCOMING_CALL_KEY


class CallControlView(BaseCallControlView):
    queryset = CallControlSerializer.Meta.model.objects.filter(call_origin='client').order_by('-created')
    filter_class = CallControlFilter
    serializer_class = CallControlSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class CallControlLeadView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CallControlLeadSerializer
    queryset = CallControlLeadSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'click2call':
            self.serializer_class = Click2CallSerializer
        return super().get_serializer_class()

    @action(methods=["POST"], detail=False)
    def click2call(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

        if self.action == 'click2call':
            LeadManagement.objects.create(
                lead=serializer.instance.lead,
                user=serializer.instance.lead.user,
                event=EVENT_OUTCOMING_CALL_KEY,
                status=serializer.instance.lead.status,
                message="Llamada emitida"
            )


class CallReceiverView(BaseCallReceiverView):

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(operation_description=_("Service to register received calls from APIVoice"))
    def call_receiver(self, request, *args, **kwargs):
        extra_data = {'call_origin': 'client'}

        dst = normalize_phone(request.data.get('dst'))
        # print('-----------------------------------------')
        # print(dst)
        # print('##########################################')
        filter_kwargs = {'source__data': dst}
        try:
            concession = get_object_or_404(Concessionaire.objects.all(), **filter_kwargs)
        except:
            filter_kwargs = {'mask_c2c': dst}
            concession = get_object_or_404(Concessionaire.objects.all(), **filter_kwargs)
        self.default_src = concession.mask_c2c.replace('+', '00') if concession.mask_c2c else None
        self.dst_phone = concession.concession_phone.replace('+', '00') if concession.concession_phone else None
        # print(concession)

        if not (request.data.get('userfield') or request.data.get('userdata')):
            parse = (request.data.get('src'), self.dst_phone)
            flow_instance = Flow.objects.get(type='flow', is_default=True)
            if not self.dst_phone:
                query = {'is_error': True}
            else:
                query = {'is_initial': True}
            command_instance = flow_instance.command_set.get(**query)
            user_field = command_instance.user_field(*parse, first_execution=True)
            extra_data.update({'userfield': user_field})

        if not request.data.get('startcall'):
            extra_data.update({'startcall': str(timezone.now())})
        # print(extra_data)
        # print('@@@@@@@@@@@@@@@@@@@@@@')
        return self.common(request, extra_data, *args, **kwargs)


class CallHistoryView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = CallControlSerializer
    queryset = CallControlSerializer.Meta.model.objects.all()
    permission_classes = [Or(IsAuthenticated)]
    filter_class = CallControlFilter
    search_fields = CallControlFilter.Meta.fields
    lookup_field = 'callcontrolleadmodel__lead__id'

    def get_queryset(self):
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        if self.action in ['incoming_calls']:
            filter_kwargs['call_origin'] = 'client'
            self.queryset = self.queryset.filter(**filter_kwargs)
        elif self.action in ['outgoing_calls']:
            filter_kwargs['call_origin'] = 'user'
            self.queryset = self.queryset.filter(**filter_kwargs)
        else:
            self.queryset = self.queryset.none()
        return super().get_queryset()

    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=True)
    def incoming_calls(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=True)
    def outgoing_calls(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
