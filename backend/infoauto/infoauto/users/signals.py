from django.db.models.signals import pre_save
from django.dispatch import receiver

from infoauto.users.models import User, SessionWithHistoric


@receiver(pre_save, sender=User)
def user_callback(sender, instance, *args, **kwargs):
    created = False if instance.id else True
    old_instance = sender.objects.get(pk=instance.pk) if not created else None
    if ((old_instance and old_instance.is_active and not instance.is_active and not created) or
            (created and not instance.is_active)):
        instance.user_deactivation_date = instance.modified
        instance.user_activation_date = None
    elif ((old_instance and not old_instance.is_active and instance.is_active and not created) or
            (created and instance.is_active)):
        instance.user_activation_date = instance.modified
        instance.user_deactivation_date = None
    else:
        pass
