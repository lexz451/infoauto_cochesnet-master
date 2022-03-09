from django_filters.rest_framework import DjangoFilterBackend
from rest_condition import Or
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from infoauto.common.permissions import IsAdminUser
from infoauto.leads.permissions import IsConcessionaireAdmin
from infoauto.source_channels.models import Source, Channel
from infoauto.source_channels.serializers import ChannelSerializer, CompleteSourceSerializer


class ChannelView(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ["id", "origin__id", "origin__name", "source_channel__concession", "source_channel__origin"]

    def check_permissions(self, request):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]

        return super().check_permissions(request)


class SourceView(ModelViewSet):
    serializer_class = CompleteSourceSerializer
    queryset = Source.objects.all().order_by("id")
    permission_classes = [Or(IsAdminUser, IsConcessionaireAdmin)]
    search_fields = ("channel__name", "origin__name", "concession__name", "data")

    def list(self, request, *args, **kwargs):
        if not request.user.is_admin:
            concessions_id = request.user.userconcession_set.all().distinct().values_list('concessionaire__id', flat=True)
            self.queryset = self.queryset.filter(concession__id__in=list(concessions_id)).distinct().order_by("id")
        return super().list(request, *args, **kwargs)

    def check_permissions(self, request):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
        else:
            self.permission_classes = [Or(IsAdminUser, IsConcessionaireAdmin)]
        return super().check_permissions(request)
