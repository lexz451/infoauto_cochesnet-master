from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from infoauto.netelip.models import CallControlModel, Command, Flow


class CallControlModelAdmin(SimpleHistoryAdmin):
    model = CallControlModel
    list_display = ['id', 'get_id_call', 'api', 'src', 'dst', 'startcall', 'durationcall', 'durationcallanswered',
                    'get_description', 'statuscode', 'statuscall', 'userdata', 'typesrc', 'usersrc', 'call_origin']

    def get_id_call(self, obj):
        return obj.id_call
    get_id_call.admin_order_field = 'id_call'
    get_id_call.short_description = 'ID'

    def get_description(self, obj):
        if obj.description and obj.description.startswith('/APIVoice/Record/'):
            link = reverse("calls-audio", args=[obj.id])
            return mark_safe('<a href="%s">%s</a>' % (link, obj.description))
        return obj.description
    get_description.admin_order_field = 'description'
    get_description.short_description = 'Description/Recorded Call'


admin.site.register(CallControlModel, CallControlModelAdmin)
admin.site.register(Flow)


class CommandAdmin(admin.ModelAdmin):
    model = Command
    list_display = ['id', 'get_flow_id', 'is_initial', 'is_error', 'command', 'options', ]

    def get_flow_id(self, obj):
        return obj.flow.id

    get_flow_id.admin_order_field = 'flow__id'
    get_flow_id.short_description = 'Flow Id'


admin.site.register(Command, CommandAdmin)
