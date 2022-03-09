from django.core.exceptions import ObjectDoesNotExist
from simple_history.models import HistoricalRecords as BaseHistoricalRecords


class HistoricalRecords(BaseHistoricalRecords):

    @staticmethod
    def get_last_historic_attribute(last_historic, attribute_name, default=None):
        try:
            return getattr(last_historic, attribute_name, default)
        except ObjectDoesNotExist:
            return True

    def get_changed_fields(self, sender, instance, history_field_name='history', avoid_fields=None):
        history = getattr(instance, history_field_name, None)
        avoid_fields = ['modified'] + (avoid_fields or [])
        if history and history.all().exists():
            last_historic = instance.history.order_by('history_id').last()
            changed_fields = []
            for i in sender._meta.fields:
                checkup = (getattr(instance, i.name, None) !=
                           self.get_last_historic_attribute(last_historic, i.name, None))
                if checkup and i.name not in avoid_fields:
                    changed_fields.append(
                        {
                            'field': i,
                            'old_value': self.get_last_historic_attribute(last_historic, i.name, None),
                            'new_value': getattr(instance, i.name, None)
                         }
                    )
        else:
            # Case - No history exists and instance is not created
            # That's occur when history added after model creation
            changed_fields = [
                {'field': i} for i in sender._meta.fields
            ]
        return changed_fields

    def post_save(self, instance, created, changeReason=None, **kwargs):
        setattr(instance, "changeReason", changeReason) if changeReason else None
        setattr(instance, 'skip_history_when_saving', True) if not changeReason else None
        return super().post_save(instance, created, **kwargs)

    def post_delete(self, instance, changeReason=None, **kwargs):
        setattr(instance, "changeReason", changeReason) if changeReason else None
        return super().post_delete(instance, **kwargs)
