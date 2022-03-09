from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from infoauto.netelip.models import Command


def change_command_queryset(sender, instance, attribute):
    exclude = {
        'id': instance.id,
        attribute: False
    }
    queryset = sender.objects.exclude(
        **exclude).filter(flow=instance.flow)
    for i in queryset:
        setattr(i, attribute, False)
        setattr(i, '_new_%s' % attribute, instance)
        i.save()


@receiver(pre_save, sender=Command)
def command_callback(sender, instance, *args, **kwargs):
    if instance.id:
        old_instance = sender.objects.get(id=instance.id)
        changed_fields = [
            i.name for i in sender._meta.fields
            if getattr(instance, i.name, None) != getattr(old_instance, i.name, None)
        ]
        for attribute in ['is_initial', 'is_error']:
            if attribute in changed_fields:
                if getattr(instance, attribute, False):
                    change_command_queryset(sender, instance, attribute)
                else:
                    query = {attribute: True, 'flow': instance.flow}
                    queryset = sender.objects.exclude(id=instance.id).filter(**query)
                    if not (queryset.exists() or getattr(instance, '_new_%s' % attribute, None)):
                        raise ValidationError({
                            attribute:
                                _("No es posible realizar esta acción.")})
    else:
        for attribute in ['is_initial', 'is_error']:
            if getattr(instance, attribute, False):
                change_command_queryset(sender, instance, attribute)


@receiver(pre_delete, sender=Command)
def check_deletion_command(sender, instance, using, *args, **kwargs):
    if instance.is_initial or instance.is_error:
        raise ValidationError(_("Esta instancia no puede ser borrada. Es un comando de 'inicio' o 'error'"))

