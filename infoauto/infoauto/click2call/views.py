from rest_condition import Or
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from infoauto.click2call.serializers import Click2CallSerializer
from infoauto.common.permissions import IsAdminUser
from infoauto.leads.models import Task
from infoauto.leads.serializers import TaskSerializer


class Click2CallView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = Click2CallSerializer
    queryset = Task.objects.all()
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = TaskSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
