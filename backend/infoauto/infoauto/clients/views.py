from rest_condition import Or
from rest_framework import mixins
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from infoauto.clients.serializers import ClientSerializer
from infoauto.common.permissions import IsAdminUser
from infoauto.leads.models import Client
from infoauto.leads.views import GenericViewSet


class ClientView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                 mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
    filter_fields = {'name': ['icontains'], 'phone': ['icontains'], 'email': ['icontains']}
    search_fields = ('name', 'phone', 'email')
