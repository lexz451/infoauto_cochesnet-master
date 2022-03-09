from rest_condition import Or
from rest_framework import mixins
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from infoauto.business_activity.business_activity_serializers import BusinessActivitySerializer, BusinessSectorSerializer
from infoauto.common.permissions import IsAdminUser

from infoauto.leads.models import BusinessActivity, Sector


class BusinessSectorView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

    serializer_class = BusinessSectorSerializer
    queryset = Sector.objects.all()
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
    search_fields = ('custom_id', 'name')


class BusinessActivityView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

    serializer_class = BusinessActivitySerializer
    queryset = BusinessActivity.objects.all()
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
    filter_fields = {'activity': ['icontains'], 'sector__name': ['icontains'], 'sector__id': ['exact']}
    search_fields = ('custom_id', 'activity', 'sector__custom_id', 'sector__name')
