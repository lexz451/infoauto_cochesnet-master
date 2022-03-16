from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from infoauto.leads.models import Request, Lead, Note, Origin, Concessionaire, Phone, Email, UserConcession, Task, \
    Client, Vehicle, Campaign

admin.site.register(Lead, SimpleHistoryAdmin)
admin.site.register(Note, SimpleHistoryAdmin)


class ClientAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'get_province', 'get_location']
    search_fields = ('id', 'name', 'phone', 'email', 'province__name', 'location__name')

    def get_province(self, obj):
        return obj.province.name if obj.province else None
    get_province.admin_order_field = 'province__id'
    get_province.short_description = 'Province'

    def get_location(self, obj):
        return obj.location.name if obj.location else None
    get_location.admin_order_field = 'location__id'
    get_location.short_description = 'Location'


admin.site.register(Client, ClientAdmin)
admin.site.register(Origin)
admin.site.register(Concessionaire)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(UserConcession)
admin.site.register(Task)
admin.site.register(Request, SimpleHistoryAdmin)
admin.site.register(Campaign)

admin.site.register(Vehicle, SimpleHistoryAdmin)
