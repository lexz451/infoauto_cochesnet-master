from drf_writable_nested import WritableNestedModelSerializer
from infoauto.leads.models.campaign import Campaign

class CampaignSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            'id',
            'name',
            'RSPCRM_campaingId',
            'RSPCRM_origin',
            'campaignType',
            'brandRange',
            'distributionBranch',
            'startDate',
            'endDate',
            'isActive',
            'key',
            'goal',
            'concessionaire',
            'productName',
            'sourceSystem',
            'status',
            'offer',
            'url',
            'communicationType',
            'legalEntityPartnerNumber',
            'origin',
            'source',
            'model',
            'version',
            'investment',
            #'user',
            'utm_campaing',
            'utm_source',
            'utm_content',
            'note',
            'expenses'
        )
    