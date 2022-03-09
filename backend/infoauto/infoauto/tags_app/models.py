from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from infoauto.common.simple_history import HistoricalRecords


class TagHistoricalRecords(HistoricalRecords):
    def post_save(self, instance, created, **kwargs):
        changed_fields = self.get_changed_fields(sender=kwargs['sender'], instance=instance)
        msg = None
        if created:
            msg = 'Un nuevo TAG ha sido dado de alta en el lead'
        elif changed_fields:
            msg = 'El TAG con fecha %s, ha sido modificado' % instance.modified.astimezone().strftime("%d/%m/%Y %H:%M")
        return super().post_save(instance, created, changeReason=msg, **kwargs)


class Tag(TimeStampedModel):
    content = TextField(blank=True, null=True)
    history = TagHistoricalRecords()

    class Meta:
        verbose_name = _("TAG")
        verbose_name_plural = _("TAGS")
