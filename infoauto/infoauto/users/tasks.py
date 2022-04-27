from celery import shared_task

from infoauto.users.models import SessionWithHistoric, User
from django.conf import settings

@shared_task
def update_session_user():
    [i.active_time_yesterday for i in SessionWithHistoric.objects.all()]


