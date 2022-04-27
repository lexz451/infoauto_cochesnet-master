from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from infoauto.leads.models import Vehicle, Appraisal, VehicleVersion, VehicleModel, VehicleBrand
from infoauto.leads.serializers.core import AppraisalSerializer
from infoauto.vehicles.serializers import VehicleSerializer, VehicleVersionSerializer, VehicleModelSerializer, \
    VehicleBrandSerializer


class VehicleView(mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated]


class AppraisalView(mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = AppraisalSerializer
    queryset = Appraisal.objects.all()
    permission_classes = [IsAuthenticated]


class VehicleVersionView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = VehicleVersionSerializer
    queryset = VehicleVersion.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filter_fields = {'version_name': ['icontains'],
                     'motor': ['icontains'],
                     'engine_power': ['icontains'],
                     'vehicle_model__model_name': ['icontains'],
                     'vehicle_model__brand__name': ['icontains'],
                     'vehicle_model__brand__id': ['exact'],
                     }
    search_fields = ('id', 'version_name', 'motor', 'engine_power', 'fuel', 'gearbox', 'vehicle_model__model_name',
                     'vehicle_model__brand__name', 'comments')
    filterset_fields = ['version_name', 'motor', 'engine_power', 'fuel', 'gearbox', 'vehicle_model__model_name',
                        'vehicle_model__brand__name', 'vehicle_model__brand__id', 'comments', 'vehicle_model__id']


class VehicleModelView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = VehicleModelSerializer
    queryset = VehicleModel.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filter_fields = {'model_name': ['icontains'],
                     'brand__name': ['icontains'],
                     }
    search_fields = ('id', 'model_name', 'brand__name')
    filterset_fields = ['model_name', 'brand__name', 'brand__id']


class VehicleBrandView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = VehicleBrandSerializer
    queryset = VehicleBrand.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filter_fields = {'name': ['icontains']}

    search_fields = ('name', )
    filterset_fields = ['name', ]

