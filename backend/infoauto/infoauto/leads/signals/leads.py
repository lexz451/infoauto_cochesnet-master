# -*- coding: utf-8 -*-

from django.db.models.signals import pre_save
from django.dispatch import receiver

from infoauto.leads.models import Lead
from infoauto.leads.utils import set_status_finish_date


@receiver(pre_save, sender=Lead)
def lead_callback(sender, instance, *args, **kwargs):
    if instance.result:
        if instance.id:
            old_instance = sender.objects.get(id=instance.id)
            if instance.result and (instance.result != old_instance.result):
                instance = set_status_finish_date(instance)
        else:
            instance = set_status_finish_date(instance)
    # force_status = popattr(instance, 'force_status', False)
    # instance.status = update_status(instance, force_status=force_status)
    # if instance.status != 'end':
    #     instance.result = None
    instance.lead_task_date = instance.first_task_date


"""
@receiver(post_save, sender=Lead)
def check_lead_actions(sender, instance, *args, **kwargs):
    if check_field_change(sender, instance, field_name='status'):
        def lead_action_change_status(lead_action):
            lead_action.status = DONE_KEY
            lead_action.save()
        [lead_action_change_status(lead_action)
         for lead_action in instance.leadaction_set.filter(
            Q(lead_status_planing=instance.status), ~Q(status=DONE_KEY))
         if lead_action.status != DONE_KEY]
"""
