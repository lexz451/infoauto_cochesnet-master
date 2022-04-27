import json

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from drf_yasg.utils import swagger_auto_schema
from rest_condition import Or
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from infoauto.common.permissions import IsAdminUser
from infoauto.leads.models import Concessionaire, Lead
from infoauto.leads.permissions import IsConcessionaireAdmin
from infoauto.leads.serializers import LeadSimpleSerializer
from infoauto.users.filters import SessionWithHistoricFilter, UserFilter
from infoauto.users.models import User, SessionWithHistoric, UserSFA

from .models import UserWhatsappTemplate
from .serializers import UserCreateSerializer, ComplexUserCreateSerializer, SetUserLeadsSerializer, \
    HistoricalSessionWithHistoricSerializer, SimpleSessionWithHistoricSerializer
from .serializers.users import SimpleUserListSerializer, SFAUserUpdateSerializer


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def user_login(user):
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except ObjectDoesNotExist:
        pass
    token, created = Token.objects.get_or_create(user=user)
    serializer = AuthTokenSerializer(user)
    data = serializer.data
    data['token'] = token.key
    user.is_available = True
    user.save()
    return Response(status=status.HTTP_200_OK, data=data)


def login(request, data):
    print("login")
    serializer = AuthTokenSerializer(data=data)
    serializer.context.update({'request': request})
    if not serializer.is_valid():
        return Response(status=status.HTTP_403_FORBIDDEN, data={
            "non_field_errors": [
                "No se puede iniciar sesión con las credenciales proporcionadas."
            ]
        })
    user = serializer.validated_data['user']
    return user_login(user)


class AuthenticationView(GenericViewSet):
    serializer_class = AuthTokenSerializer
    queryset = User.objects.all()

    def check_permissions(self, request):
        if self.action in ["login_as_user"]:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['logout']:
            self.permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
        return super().check_permissions(request)

    def get_serializer_class(self):
        if not getattr(self, 'swagger_fake_view', False):
            if self.action in ['login_as_user', 'logout']:
                self.serializer_class = None
        return super().get_serializer_class()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: json.dumps({"username": "string", "password": "string", "token": "string"}),
                   status.HTTP_201_CREATED: None,
                   status.HTTP_403_FORBIDDEN: json.dumps({
                       "non_field_errors": "No se puede iniciar sesión con las credenciales proporcionadas."})}
    )
    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        return login(request, data=request.data)

    @action(methods=['post'], detail=True)
    def login_as_user(self, request, *args, **kwargs):
        user = self.get_object()
        return user_login(user)

    @swagger_auto_schema(
        request_body=None,
        responses={status.HTTP_200_OK: "",
                   status.HTTP_201_CREATED: None}
    )
    @action(methods=['post'], detail=False)
    def logout(self, request, *args, **kwargs):
        self.queryset = User.objects.all()
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = request.user
            token = Token.objects.get(user=user)
            token.delete()
            user.is_available = False
            user.save()
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class SFAView(GenericViewSet, mixins.DestroyModelMixin):
    queryset = UserSFA.objects.all()
    permission_classes = [Or(IsConcessionaireAdmin, DjangoModelPermissions)]


class UserWhatsappTemplateView(GenericViewSet, mixins.DestroyModelMixin):
    queryset = UserWhatsappTemplate.objects.all()
    permission_classes = [Or(IsConcessionaireAdmin, DjangoModelPermissions)]


class UserView(GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
               mixins.ListModelMixin):
    serializer_class = ComplexUserCreateSerializer
    queryset = User.objects.all()
    filter_class = UserFilter
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'userconcession__concessionaire__id')

    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = UserCreateSerializer
        elif self.action in ['set_user_leads']:
            self.serializer_class = SetUserLeadsSerializer
        return super().get_serializer_class()

    def check_permissions(self, request):
        if self.action in ['list', 'current_user', 'concession_manager_or_admin', 'list_user_leads', 'complex_update']:
            self.permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
        elif self.action in ['complex_create', 'complex_update', 'update', 'partial_update', 'create', 'set_user_leads']:
            self.permission_classes = [IsConcessionaireAdmin]
        else:
            self.permission_classes = []
        return super(UserView, self).check_permissions(request)

    def list(self, request, *args, **kwargs):
        if request.GET.get('is_complex') == "false":
            self.serializer_class = SimpleUserListSerializer

        if not request.user.is_admin:
            concessions_id = request.user.userconcession_set.all().distinct().values_list(
                'concessionaire__id', flat=True)
            self.queryset = self.queryset.filter(
                userconcession__concessionaire__id__in=list(concessions_id)
            ).distinct().order_by("id")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code != 201:
            return response
        return login(request, data={'username': request.data.get('email'), 'password': request.data.get('password')})

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request=request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def complex_create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code != 201:
            return response
        return login(request, data={'username': request.data.get('email'), 'password': request.data.get("password")})

    @action(methods=['PATCH'], detail=True)
    def complex_update(self, request, *args, **kwargs):
        if not (request.user.is_admin or request.user.is_superuser or request.user.userconcession_set.filter(is_concessionaire_admin=True).exists()):
            self.serializer_class = SFAUserUpdateSerializer
        return super().partial_update(request=request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def current_user(self, request, *args, **kwargs):
        self.lookup_field = 'pk'
        self.kwargs['pk'] = request.user.id
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description=("<h2>Get users from Concessionaire with special permissions. "
                                                "Required parameter: Concessionaire ID</h2>"))
    @action(methods=["GET"], detail=True)
    def concession_manager_or_admin(self, request, *args, **kwargs):
        concessionaire = get_object_or_404(Concessionaire.objects.all(), **self.kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, concessionaire)
        query = (Q(userconcession__concessionaire=concessionaire, userconcession__is_business_manager=True) |
                 Q(userconcession__concessionaire=concessionaire, userconcession__is_concessionaire_admin=True))
        self.queryset = User.objects.filter(query).distinct().order_by('id')
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LeadSimpleSerializer})
    @action(methods=['GET'], detail=True)
    def list_user_leads(self, request, *args, **kwargs):
        user = self.get_object()
        queryset = Lead.objects.filter(user=user)
        serializer = LeadSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def set_user_leads(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)


class HistoricalSessionWithHistoricView(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    model = HistoricalSessionWithHistoricSerializer.Meta.model
    serializer_class = HistoricalSessionWithHistoricSerializer
    queryset = model.objects.all()
    permission_classes = [Or(IsAdminUser, IsConcessionaireAdmin)]
    filter_class = SessionWithHistoricFilter

    def get_serializer_class(self):
        if self.action in ['change_forced_online_status']:
            self.serializer_class = SimpleSessionWithHistoricSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action in ['my_historic']:
            try:
                self.queryset = self.model.objects.filter(
                    user=self.request.user, id=self.request.user.sessionwithhistoric.id)
            except Exception:
                self.queryset = self.model.objects.none()
        return super().get_queryset()

    def check_permissions(self, request):
        if self.action in ['my_historic']:
            self.permission_classes = [Or(IsAdminUser, DjangoModelPermissions, IsAuthenticated)]
        return super().check_permissions(request=request)

    @action(methods=['GET'], detail=False)
    def my_historic(self, request, *args, **kwargs):
        return super().list(request=request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user_id = request.GET.get('user__id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = None
            if user:
                try:
                    self.queryset = self.queryset.filter(id=user.sessionwithhistoric.id)
                except Exception:
                    self.queryset = self.queryset.none()
            else:
                self.queryset = self.queryset.none()
        return super().list(request, *args, **kwargs)

    @action(methods=['PATCH'], detail=False)
    def change_forced_online_status(self, request, *args, **kwargs):
        self.filter_class = None
        self.kwargs['pk'] = request.user.sessionwithhistoric.pk
        self.queryset = SessionWithHistoric.objects.all()
        return super().partial_update(request, *args, **kwargs)
