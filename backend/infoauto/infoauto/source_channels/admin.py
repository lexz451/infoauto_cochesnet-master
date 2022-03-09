from django.contrib import admin

from .models import Channel, Source


class ChannelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Channel, ChannelAdmin)


class SourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Source, SourceAdmin)
