from django.db.models.signals import post_save
from django.dispatch import receiver

from infoauto.leads.models import Task


@receiver(post_save, sender=Task)
def task_callback(sender, instance, *args, **kwargs):
    leads = sender.objects.none()
    for i in instance.request_set.all():
        if leads:
            leads = leads | i.lead_set.all()
        else:
            leads = i.lead_set.all()
    if leads:
        [i.task_date(save_instance=True) for i in leads.distinct()]
