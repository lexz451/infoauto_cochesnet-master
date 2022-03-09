from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from simple_history.admin import SimpleHistoryAdmin

from infoauto.users.models import SessionWithHistoric
from .forms import UserChangeForm, UserCreationForm

User = get_user_model()

"""
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser"]
    search_fields = ["username"]
"""
admin.site.register(User, SimpleHistoryAdmin)
admin.site.register(SessionWithHistoric, SimpleHistoryAdmin)
