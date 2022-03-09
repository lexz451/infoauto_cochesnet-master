
from django.db.models import Q
from rest_condition import Or
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet

from infoauto.common.permissions import IsAdminUser
from infoauto.concessionaires.serializers import UserConcessionSerializer, PhoneSerializer, ConcessionaireSerializer, \
    ListPhoneSerializer, EmailSerializer, ListEmailSerializer, ConcessionDashboardSerializer, \
    SimpleConcessionaireSerializer
from infoauto.leads.models import UserConcession, Phone, Concessionaire, LEAD_STATUS, LEAD_RESULT, Email
from infoauto.leads.permissions import IsConcessionaireAdmin


class ConcessionaireView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                         mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ConcessionaireSerializer
    queryset = Concessionaire.objects.all().order_by('id')
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
    filter_fields = {}
    search_fields = ('source__data', 'source__origin__name', 'source__channel__name', 'name')

    def list(self, request, *args, **kwargs):
        if request.GET.get('is_complex') == "false":
            self.serializer_class = SimpleConcessionaireSerializer

        if not request.user.is_admin:
            concessions_id = request.user.userconcession_set.all().distinct().values_list('concessionaire__id', flat=True)
            self.queryset = self.queryset.filter(id__in=list(concessions_id)).distinct().order_by("id")
        return super().list(request, *args, **kwargs)

    def get_lead_queryset(self, queryset):
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            queryset = queryset.filter(
                Q(concessionaire__user__id=self.request.user.id,
                  concessionaire__userconcession__is_concessionaire_admin=True
                  ) | Q(
                    concessionaire__user__id=self.request.user.id,
                    concessionaire__userconcession__is_business_manager=True
                ) | Q(user__id=self.request.user.id))\
                .distinct().order_by('id')
        return queryset

    @action(methods=['GET'], detail=False)
    def config(self, request, *args, **kwargs):
        if not request.user.is_admin:
            self.queryset = self.queryset.filter(
                Q(userconcession__is_concessionaire_admin=True), user=request.user).distinct().order_by("id")
        return super().list(request, *args, **kwargs)

    def check_permissions(self, request):
        if self.action in ['config', 'update']:
            self.permission_classes = [IsConcessionaireAdmin]
        elif self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
        return super().check_permissions(request)


class UserConcessionView(mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = UserConcessionSerializer
    queryset = UserConcession.objects.all()
    permission_classes = [Or(IsAdminUser, IsConcessionaireAdmin)]


class PhoneView(mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = PhoneSerializer
    queryset = Phone.objects.filter(concessionaire__isnull=False).order_by("id")
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
    filter_fields = {'number': ['icontains'], 'concessionaire__name': ['icontains']}
    search_fields = ('number', 'concessionaire__name', 'origin__name')

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = ListPhoneSerializer
        return super().get_serializer_class()

    def check_permissions(self, request):
        if self.action == 'destroy':
            self.permission_classes = [IsConcessionaireAdmin]
        return super().check_permissions(request)


class EmailView(mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = EmailSerializer
    queryset = Email.objects.filter(concessionaire__isnull=False).order_by("id")
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
    filter_fields = {'email': ['icontains'], 'concessionaire__name': ['icontains']}
    search_fields = ('email', 'concessionaire__name', 'origin__name')

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = ListEmailSerializer
        return super().get_serializer_class()

    def check_permissions(self, request):
        if self.action == 'destroy':
            self.permission_classes = [IsConcessionaireAdmin]
        return super().check_permissions(request)


class ConcessionDashboardEmail(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Concessionaire.objects.all().order_by("id")
    serializer_class = ConcessionDashboardSerializer
    permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            self.queryset = Concessionaire.objects.all().order_by("id")
        elif self.request.user.is_authenticated and self.request.user.is_concession_admin:
            self.queryset = self.request.user.concessionaire_set.all().order_by("id")
        else:
            self.queryset = self.queryset.none()
        return super().get_queryset()
