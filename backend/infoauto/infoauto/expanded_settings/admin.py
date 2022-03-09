import ast

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm, CharField, Textarea, Form

from infoauto.expanded_settings.models import Setting


class SettingForm(ModelForm):
    name = CharField()
    value_aux = CharField(widget=Textarea, label='value')

    class Meta:
        model = Setting
        fields = ('name', 'value_aux', )

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            kwargs['initial'] = {'value_aux': str(kwargs['instance'].value)}
        super().__init__(*args, **kwargs)

    def clean(self):
        value_aux = self.cleaned_data.pop('value_aux', None)
        try:
            value = ast.literal_eval(value_aux)
        except (ValueError, SyntaxError):
            value = value_aux
        self.cleaned_data['value'] = value
        return super().clean()

    def save(self, commit=True):
        self.instance.value = self.cleaned_data['value']
        return super().save(commit)


class SettingAdmin(ModelAdmin):
    form = SettingForm
    add_form = SettingForm
    list_display = ['id', 'name', 'value']
    search_fields = ('id', 'name', 'value')


admin.site.register(Setting, SettingAdmin)
