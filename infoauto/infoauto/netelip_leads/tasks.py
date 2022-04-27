from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _

from infoauto.common.util_email import send_email
from infoauto.netelip.models import CallControlModel
from infoauto.source_channels.models import Source

app = Celery()


def email_advise(instance):
    current_site = get_current_site(request=None)
    source = Source.objects.get(data=instance.dst)
    context = {'call': instance, 'source': source, 'current_site': current_site,
               'msg': "La llamada mostrada a continuación lleva un tiempo sin supervisión"}
    to_email = getattr(settings, 'EMAILS_FORGOTTEN_CALL', None)
    send_email(to_email=to_email,
               subject=_("SAIL - Llamada sin supervisión"),
               template="email/netelip_received_call",
               context=context, smtp_config_name='default')


@shared_task
def check_lead(instance_id):
    instance = CallControlModel.objects.get(id=instance_id)
    email_advise(instance)

