from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from infoauto.netelip_leads.models import CallControlLeadModel


class CallControlLeadAdmin(admin.ModelAdmin):
    model = CallControlLeadModel
    list_display = ['id', 'get_lead', 'get_call_control']

    def get_lead(self, obj):
        link = reverse("admin:leads_lead_change", args=[obj.lead.id])
        return mark_safe('<a href="%s">%s</a>' % (link, obj.lead.id))
    get_lead.allow_tags = True
    get_lead.admin_order_field = 'lead__id'
    get_lead.short_description = 'Lead Id'

    def get_call_control(self, obj):
        link = reverse("admin:netelip_callcontrolmodel_change", args=[obj.call_control.id])
        return mark_safe('<a href="%s">%s - (%s)</a>' % (link, obj.call_control.id, obj.call_control.id_call))
    get_call_control.allow_tags = True
    get_call_control.admin_order_field = 'call_control__id'
    get_call_control.short_description = 'Call Control Id'


admin.site.register(CallControlLeadModel, CallControlLeadAdmin)
