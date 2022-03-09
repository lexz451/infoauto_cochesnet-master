# Use this as a starting point for your project with celery.
# If you are not using celery, you can remove this app
import os
from celery import Celery, shared_task
from django.apps import apps, AppConfig
from django.conf import settings
from celery.schedules import crontab
import environ
import logging

from django.utils import timezone

logger = logging.getLogger(__name__)

env = environ.Env()
IS_DOCKER = env.bool('USE_DOCKER', default=False)

if IS_DOCKER:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.docker")

elif not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.local')

app = Celery('match')


class CeleryAppConfig(AppConfig):
    name = 'infoauto.taskapp'
    verbose_name = 'Celery Config'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def test_task1():
    logger.info("test_task")
    print("test_task")


@shared_task
def change_users_status_to_inactive():
    from infoauto.users.models import User

    User.objects.all().update(is_available=False)
    logger.info("[CELERY BEAT] Run change_users_status_to_inactive.")


@shared_task
def ubunet_calls():
    from infoauto.netelip.utils import ubunet_calls
    ubunet_calls()


@shared_task
def check_all_incoming_calls_is_duplicated():
    from infoauto.netelip.utils import check_calls

    check_calls()
    logger.info("[CELERY BEAT] Run check_all_incoming_calls_is_duplicated.")


@shared_task
def persistir_maestro():
    from django.db import connection
    cursor = connection.cursor()
    try:
        cursor.execute('''drop table MASTER_INFOAUTO_PERSISTENTE''')
    except:
        pass

    try:
        cursor.execute('''CREATE TABLE MASTER_INFOAUTO_PERSISTENTE SELECT * FROM MASTER_INFOAUTO_VIEW''')
    except:
        pass

    try:
        cursor.execute('''update netelip_callcontrolmodel set is_checked=0 where call_origin='user' and id not in (select call_control_id from netelip_leads_callcontrolleadmodel) and created > date_sub(now(), interval 1 day)''')
    except:
        pass


    logger.info("[CELERY BEAT] Run Persistir maestro.")


@app.on_after_configure.connect
def add_periodic(sender, **kwargs):

    # Test task
    #sender.add_periodic_task(schedule=5, sig=test_task1, name="test")

    # Revisa todas las llamadas entrantes de los clientes, para intentar asignarles un lead,
    # en base al telefono origen y destino.
    # sender.add_periodic_task(schedule=500, sig=check_all_incoming_calls_is_duplicated, name="check_all_incoming_calls_is_duplicated")

    sender.add_periodic_task(
        crontab(
            hour=settings.AUTO_DISABLE_USER_TIME1_HOUR,
            minute=settings.AUTO_DISABLE_USER_TIME1_MINUTE
        ),
        sig=change_users_status_to_inactive,
        name="change_users_status_to_inactive_1430"
    )

    sender.add_periodic_task(
        crontab(
            hour=settings.AUTO_DISABLE_USER_TIME2_HOUR,
            minute=settings.AUTO_DISABLE_USER_TIME2_MINUTE
        ),
        sig=change_users_status_to_inactive,
        name="change_users_status_to_inactive_2030"
    )

    sender.add_periodic_task(
        schedule=60,
        sig=ubunet_calls,
        name="ubunet_calls"
    )

    sender.add_periodic_task(
        schedule=60*60,
        sig=persistir_maestro,
        name="persistir_maestro"
    )
