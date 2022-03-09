# -*- coding: utf-8 -*-


from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from infoauto.netelip.models import Flow


def change_default_flow_queryset(sender, instance):
    queryset = sender.objects.exclude(
        id=instance.id, is_default=False).filter(
        type=instance.type)
    for i in queryset:
        i.is_default = False
        setattr(i, '_new_default', instance)
        i.save()


@receiver(pre_save, sender=Flow)
def flow_callback(sender, instance, *args, **kwargs):
    if instance.id:
        old_instance = sender.objects.get(id=instance.id)
        changed_fields = [
            i.name for i in sender._meta.fields
            if getattr(instance, i.name, None) != getattr(old_instance, i.name, None)
        ]
        if 'is_default' in changed_fields:
            if instance.is_default:
                change_default_flow_queryset(sender, instance)
            else:
                queryset = sender.objects.exclude(id=instance.id).filter(type=instance.type, is_default=True)
                if not (queryset.exists() or getattr(instance, '_new_default', None)):
                    raise ValidationError({
                        'is_default':
                            _("No es posible realizar esta acción. "
                              "Debe definirse un nuevo flujo por defecto para el tipo '%s'"
                              "" % instance.get_type_display())})
    else:
        if instance.is_default:
            change_default_flow_queryset(sender, instance)


@receiver(pre_delete, sender=Flow)
def check_deletion_flow(sender, instance, using, *args, **kwargs):
    if instance.is_default:
        raise ValidationError(_("Este comando no puede ser borrado. Es un flujo por defecto"))

