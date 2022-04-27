from django.apps import apps
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from infoauto.leads.models import Lead, Concessionaire, UserConcession, Phone
from infoauto.source_channels.models import Source
from infoauto.users.admin import User


class IsConcessionaireAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return is_authenticated
        try:
            instance = view.get_object()
        except AssertionError:
            instance = None
            if request.user.is_admin or request.user.is_concession_admin:
                result = True
            else:
                result = False
        if instance:
            query = Q(user__id=request.user.id, is_concessionaire_admin=True)
            if request.user.is_admin:
                result = True
            elif isinstance(instance, Lead):
                if instance.user == request.user:
                    result = True
                else:
                    result = instance.concessionaire.userconcession_set.filter(query).exists()
            elif isinstance(instance, Concessionaire):
                result = instance.userconcession_set.filter(query).exists()
            elif isinstance(instance, UserConcession):
                result = instance.concessionaire.userconcession_set.filter(query).exists()
            elif isinstance(instance, User):
                concessionaries = request.user.userconcession_set.filter(query).values_list('concessionaire', flat=True)
                result = instance.userconcession_set.filter(concessionaire__in=concessionaries).exists()
            elif isinstance(instance, Phone):
                aux = instance.concessionaire_set.order_by('id').first()
                if aux:
                    result = aux.userconcession_set.filter(query, concessionaire=aux).exists()
                else:
                    result = False
            elif isinstance(instance, Source):
                result = instance.concession.userconcession_set.filter(query).exists()
            elif isinstance(instance, apps.get_model('users', model_name='HistoricalSessionWithHistoric')):
                concessionaries = request.user.userconcession_set.filter(query).values_list('concessionaire', flat=True)
                result = instance.user.userconcession_set.filter(concessionaire__in=concessionaries).exists()
            else:
                result = True
        return result


class IsBusinessManager(IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return is_authenticated
        try:
            instance = view.get_object()
        except AssertionError:
            instance = None
            if request.user.is_admin or request.user.is_concession_admin:
                result = True
            else:
                result = False
        if instance:
            query = Q(user__id=request.user.id, is_business_manager=True)
            if request.user.is_admin:
                result = True
            elif isinstance(instance, Lead):
                if instance.user == request.user:
                    result = True
                else:
                    result = instance.concessionaire.userconcession_set.filter(query).exists()
            elif isinstance(instance, Concessionaire):
                result = instance.userconcession_set.filter(query).exists()
            elif isinstance(instance, UserConcession):
                result = instance.concessionaire.userconcession_set.filter(query).exists()
            elif isinstance(instance, User):
                concessionaries = request.user.userconcession_set.all().values_list('concessionaire', flat=True)
                result = instance.userconcession_set.filter(concessionaire__in=concessionaries).exists()
            elif isinstance(instance, Phone):
                aux = instance.concessionaire_set.order_by('id').first()
                if aux:
                    result = aux.userconcession_set.filter(query, concessionaire=aux).exists()
                else:
                    result = False
            else:
                result = True
        return result
