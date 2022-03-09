
from collections import namedtuple
from django.conf import settings

from infoauto.expanded_settings.models import Setting


try:
    expanded_settings = dict(Setting.objects.values_list('name', 'value'))
except:
    expanded_settings = {}

settings_dict = settings.__dict__['_wrapped'].__dict__
settings_dict.update(expanded_settings)
keys = settings_dict.keys()
keys = set(keys)
[settings_dict.pop(i) for i in keys if i.startswith('_')]
settings = namedtuple("Settings", settings_dict.keys())(*settings_dict.values())



