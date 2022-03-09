
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_condition import Or
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from infoauto.netelip.models import Flow, CallControlModel
from infoauto.netelip.utils import get_recorded_call, get_record_file_name
from infoauto.netelip.client import CallProcess as CallProcessBase
from infoauto.netelip.filters import CallControlFilter
from infoauto.netelip.serializers import CallControlSerializer


class CallProcess(CallProcessBase):
    default_src = ''

    def validate_callerid(self, data):
        if data.get('description') == 'CallerID is not updated':
            self.src = self.default_src
        return True


class CallReceiverView(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet, CallProcess):
    serializer_class = CallControlSerializer
    queryset = CallControlSerializer.Meta.model.objects.all().order_by('-id')
    permission_classes = [AllowAny]
    lookup_field = 'id_call'
    # Phone to be called in last instance
    dst_phone = None

    @staticmethod
    def set_extra_data(data, extra_data):
        if getattr(data, '_mutable', None) is False:
            data._mutable = True
        data.update(extra_data)
        if getattr(data, '_mutable', None):
            data._mutable = False

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def common(self, request, extra_data, *args, **kwargs):
        if request.data.get('description', '').startswith("/APIVoice/"):
            data = {'command': 'hangout', 'options': '', 'userfield': ''}
        else:
            self.set_extra_data(data=request.data, extra_data=extra_data)
            data = self.get_operation(request.data)
        # print(request.data)
        # print(data)
        self.kwargs[self.lookup_field] = request.data.get('ID')
        if CallControlModel.objects.filter(id_call=request.data.get('ID')).exists():
            super().partial_update(request, *args, **kwargs)
        else:
            super().create(request, *args, **kwargs)

        # print(data)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(operation_description=_("Service to register realized calls with APIVoice"))
    def call_realization(self, request, *args, **kwargs):
        extra_data = {'call_origin': 'user'}
        if not request.data.get('startcall'):
            extra_data.update({'startcall': str(timezone.now())})

        return self.common(request, extra_data, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(operation_description=_("Service to register received calls from APIVoice"))
    def call_receiver(self, request, *args, **kwargs):
        extra_data = {'call_origin': 'client'}
        if not (request.data.get('userfield') or request.data.get('userdata')):
            parse = (request.data.get('src'), self.dst_phone)
            flow_instance = Flow.objects.get(type='flow', is_default=True)
            command_instance = flow_instance.command_set.get(is_initial=True)
            user_field = command_instance.user_field(*parse, first_execution=True)
            extra_data.update({'userfield': user_field})
        return self.common(request, extra_data, *args, **kwargs)


class CallControlView(ReadOnlyModelViewSet):
    serializer_class = CallControlSerializer
    queryset = CallControlSerializer.Meta.model.objects.all().order_by('id')
    permission_classes = [Or(IsAuthenticated)]
    filter_class = CallControlFilter

    @action(methods=["GET"], detail=True)
    def audio(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.ubunet_audio_downloaded:
            local_path = settings.MEDIA_ROOT + 'audios/' + str(int(instance.id_call)) + '.mp3'
        else:
            local_path = get_recorded_call(instance)
        if local_path:
            with open(local_path, 'rb') as local_file:
                file_bytes = local_file.read()
            response = HttpResponse(content=file_bytes)
            response['Content-Type'] = 'audio/mpeg3'
            response['Content-Disposition'] = 'attachment; filename="%s"' % (str(instance.id_call) + '.mp3')
            return response
        return Response()
