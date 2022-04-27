import datetime

import pytz
from django.conf import settings

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from infoauto.common.signals import check_field_change
from infoauto.leads.models.leads import LeadAction, NORMAL_KEY, WARNING_KEY, IMMEDIATE_KEY


@receiver(pre_save, sender=LeadAction)
def set_status(sender, instance, *args, **kwargs):
    if not instance.id or (instance.id and not check_field_change(sender, instance, field_name='status')):
        date = instance.date.astimezone(pytz.timezone(settings.TIME_ZONE))
        date_now = datetime.datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE))
        if date >= (date_now + datetime.timedelta(days=5)):
            instance.status = NORMAL_KEY
        elif date >= (date_now + datetime.timedelta(days=3)):
            instance.status = WARNING_KEY
        else:
            instance.status = IMMEDIATE_KEY


@receiver(post_save, sender=LeadAction)
def change_tasks_user(sender, instance, created, *args, **kwargs):
    """
    if created:
        for i in instance.lead.request.task.all():
            i.user = instance.user
            i.save()
    """
    pass
