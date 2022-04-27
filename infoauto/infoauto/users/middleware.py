from django.utils import timezone
from rest_framework.authtoken.models import Token

from infoauto.users.models import SessionWithHistoric


class LastActionUserMiddleware():

    def __init__(self, get_response, *args, **kwargs):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Process current user for update his activity
        :param request: request
        :return:
        """
        user = None
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            try:
                token = token.replace('Token ', '')
                token_instance = Token.objects.get(key=token)
                user = token_instance.user
            except Token.DoesNotExist:
                pass
        if user:
            now = timezone.now()
            user.last_action_date = now
            user.save()


class ActiveUserMiddleware():

    def __init__(self, get_response, *args, **kwargs):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Process current user for update his activity
        :param request: request
        :return:
        """
        user = None
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            try:
                token = token.replace('Token ', '')
                token_instance = Token.objects.get(key=token)
                user = token_instance.user
            except Token.DoesNotExist:
                pass
        if user:
            now = timezone.now()
            try:
                swh = user.sessionwithhistoric
            except SessionWithHistoric.DoesNotExist:
                swh = SessionWithHistoric(user=user)
                swh.skip_history_when_saving = True
                swh.save()
            swh.check_last_seen()
            swh.skip_history_when_saving = True  # Avoid update historic
            if swh.end_working or not (swh.end_working or swh.start_working):
                swh.end_working = None
                swh.start_working = now
            swh.last_seen = now
            swh.save()
