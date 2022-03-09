from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from infoauto.leads.models import ACD


class IncomingCallZadarmaView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ACD
    queryset = ACD.objects.all()

    def get_serializer_class(self):
        if not getattr(self, 'swagger_fake_view', False):
            if self.action == 'list':
                self.serializer_class = serializers.Serializer
        else:
            self.serializer_class = serializers.Serializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        """Script allowing connection with Zadarma"""
        if not request.GET.get('zd_echo'):
            raise ValidationError(_("Error en la petición"))
        return HttpResponse(request.GET['zd_echo'])

    def create(self, request, *args, **kwargs):
        # return super().create(request, *args, **kwargs)
        raise NotImplementedError("Function not implemented")
