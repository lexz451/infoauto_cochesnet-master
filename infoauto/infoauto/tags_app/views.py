from rest_condition import Or
from rest_framework.permissions import IsAdminUser, IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from infoauto.tags_app.serializers import TagSerializer


class TagView(ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [Or(IsAdminUser, IsAuthenticated, DjangoModelPermissions)]
