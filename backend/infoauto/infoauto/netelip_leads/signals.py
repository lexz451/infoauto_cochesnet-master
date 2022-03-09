
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from infoauto.common.util_email import send_email
from infoauto.netelip.models import CallControlModel
from infoauto.netelip_leads.tasks import check_lead
from infoauto.source_channels.models import Source


def email_advise(instance):
    current_site = get_current_site(request=None)
    source = Source.objects.get(data=instance.dst)
    context = {'call': instance, 'source': source, 'current_site': current_site,
               'msg': "Se ha recibido una nueva llamada con los siguientes datos"}
    to_email = getattr(settings, 'NL_EMAIL_HOST_USER', None)
    send_email(to_email=to_email,
               subject=_("SML - Nueva llamada entrante"),
               template="email/netelip_received_call",
               context=context, smtp_config_name='default')


@receiver(post_save, sender=CallControlModel)
def received_call_callback(sender, instance, created, *args, **kwargs):
    if created and instance.typesrc == 'did':
        email_advise(instance)
        transaction.on_commit(lambda: check_lead.apply_async((instance.id, ), countdown=60*5))


