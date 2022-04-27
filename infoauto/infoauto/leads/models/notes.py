# -*- coding: utf-8 -*-

from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from infoauto.common.simple_history import HistoricalRecords


class NoteHistoricalRecords(HistoricalRecords):
    def post_save(self, instance, created, **kwargs):
        changed_fields = self.get_changed_fields(sender=kwargs['sender'], instance=instance)
        msg = None
        if created:
            msg = 'Una nueva nota ha sido dada de alta en el lead'
        elif changed_fields:
            msg = 'La nota con fecha %s, ha sido modificada' % instance.modified.astimezone().strftime("%d/%m/%Y %H:%M")
        return super().post_save(instance, created, changeReason=msg, **kwargs)


class Note(TimeStampedModel):
    content = TextField()
    history = NoteHistoricalRecords()

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    @property
    def user(self):
        from infoauto.leads.models import Lead

        try:
            return self.history.filter(history_type='+').first().history_user
        except AttributeError:
            lead = Lead.objects.filter(note__in=[self.id]).first()
            if lead:
                return lead.user
