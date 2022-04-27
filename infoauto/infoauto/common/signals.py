from collections import defaultdict
from django.db.models.signals import *

def get_changed_fields(sender, instance, old_instance):
    changed_fields = [i.name for i in sender._meta.fields
                      if getattr(instance, i.name, None) != getattr(old_instance, i.name, None)]
    return changed_fields


def check_field_change(sender, instance, old_instance=None, field_name=''):
    old_instance = old_instance or getattr(instance, '_old_instance', None)
    if old_instance:
        changed_fields = get_changed_fields(sender, instance, old_instance)
        return field_name in changed_fields
    return True


def set_old_instance(sender, instance, *args, **kwargs):
    """
    Take old instance to use in post_save
    :param sender:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    if instance.id:
        setattr(instance, '_old_instance', sender.objects.get(id=instance.id))



class DisableSignals(object):
    def __init__(self, disabled_signals=None):
        self.stashed_signals = defaultdict(list)
        self.disabled_signals = disabled_signals or [
            pre_init, post_init,
            pre_save, post_save,
            pre_delete, post_delete,
            pre_migrate, post_migrate,
        ]

    def __enter__(self):
        for signal in self.disabled_signals:
            self.disconnect(signal)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for signal in list(self.stashed_signals):
            self.reconnect(signal)

    def disconnect(self, signal):
        self.stashed_signals[signal] = signal.receivers
        signal.receivers = []

    def reconnect(self, signal):
        signal.receivers = self.stashed_signals.get(signal, [])
        del self.stashed_signals[signal]