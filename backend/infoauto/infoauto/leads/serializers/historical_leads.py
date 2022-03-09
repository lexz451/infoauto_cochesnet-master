from django.apps import apps
from drf_writable_nested import WritableNestedModelSerializer


class HisoricalLeadSerializer(WritableNestedModelSerializer):
    class Meta:
        model = apps.get_model('leads', model_name='HistoricalLead')
        fields = ('id', 'created', 'modified', 'concession_phone', 'concession_email', 'status', 'end_date', 'result',
                  'finish_date', 'score', 'mail_content', 'lead_task_date', 'client', 'request', 'user',
                  'concessionaire', 'source', 'history_id', 'history_change_reason', 'history_date', 'history_user',
                  'history_type')
