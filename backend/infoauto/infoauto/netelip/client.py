import json
import urllib

import requests
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from infoauto.expanded_settings.settings import settings
from infoauto.netelip.models import Flow, Command

""" Example full URL:
http://apps.netelip.com/clicktocall/api2/api2.php
?callback=jQuery111109960860504457802_1552479887667
&netelip_c2c_telephone=6XXXXXXXX
&netelip_c2c_atk=366334ba52e294da543bca4bcb8ca43c
&netelip_c2c_destination=
&netelip_c2c_action=call
&netelip_c2c_btnid=3054
&netelip_c2c_url=http%3A%2F%2Flocalhost%3A3000%2Fleads%2F0%2Fedit
&netelip_c2c_debug=true
&_=1552479887669"""


class Click2CallClient(object):
    base_url = "http://apps.netelip.com/clicktocall/api2/api2.php"
    """?netelip_c2c_telephone=620965568
    &netelip_c2c_atk=366334ba52e294da543bca4bcb8ca43c
    &netelip_c2c_action=call
    &netelip_c2c_btnid=3054"""

    def __init__(self, atk=None, btnid=None):
        self.atk = atk or getattr(settings, 'netelip_c2c_atk', '366334ba52e294da543bca4bcb8ca43c')
        self.btnid = btnid or getattr(settings, 'netelip_c2c_btnid', '3054')

    def _api_call(self, method='get', action='call', phone=None):
        params = {
            'netelip_c2c_action': action,
            'netelip_c2c_atk': self.atk,
            'netelip_c2c_btnid': self.btnid,
            'netelip_c2c_telephone': phone
        }
        str_params = urllib.parse.urlencode(params)
        url = "%s?%s" % (self.base_url, str_params)
        response = getattr(requests, method, 'get')(url=url)
        data = response
        return data

    def c2c(self, phone):
        return self._api_call(phone=phone)


class UbunetToken(object):
    base_url = "https://pbx.smartmotorlead.net:1443/api/v2/login"

    @staticmethod
    def get_token():
        params = {
            'email': 'sclemente@info-auto.es',
            'password': 'soSYm1Pc3+rp'
        }
        response = requests.post(url=UbunetToken.base_url, json=params)
        # print(response.content)
        return json.loads(response.content).get("access_token")


class Click2CallUbunetClient(object):

    def _api_call(self, company=None, extension=None, phone=None):
        params = {
            'company': company,
            'type': 'mobile' if extension[0] == 'M' else 'user',
            'extension': extension[1:],
            'destination': phone
        }
        headers = {
            'Authorization': 'Bearer ' + UbunetToken.get_token()
        }
        base_url = "https://pbx.smartmotorlead.net:1443/api/v2/manager/call"
        response = requests.post(url=base_url, json=params, headers=headers)
        return response

    def c2c(self, company, extension, phone):
        return self._api_call(company=company, extension=extension, phone=phone)

    def get_calls(self):
        params = {}
        headers = {
            'Authorization': 'Bearer ' + UbunetToken.get_token()
        }
        base_url = "https://pbx.smartmotorlead.net:1443/api/v2/queuecdr?order=-time&limit=20&page=1"
        response = requests.post(url=base_url, json=params, headers=headers)
        return response

    def get_outgoing_calls(self):
        params = {}
        headers = {
            'Authorization': 'Bearer ' + UbunetToken.get_token()
        }
        base_url = "https://pbx.smartmotorlead.net:1443/api/v2/cdr?order=-calldate&limit=200&page=1"
        response = requests.post(url=base_url, json=params, headers=headers)
        return response

    def download_audio(self, call_id):
        headers = {
            'Authorization': 'Bearer ' + UbunetToken.get_token()
        }
        base_url = "https://pbx.smartmotorlead.net:1443/api/v2/queuecdr/record/download/" + str(call_id)
        response = requests.get(url=base_url, headers=headers)
        return response

    def download_audio_c2c(self, call_id):
        headers = {
            'Authorization': 'Bearer ' + UbunetToken.get_token()
        }
        base_url = "https://pbx.smartmotorlead.net:1443/api/v2/cdr/record/download/" + str(-call_id)
        response = requests.get(url=base_url, headers=headers)
        try:
            response = requests.get(url=json.loads(response.content).get("url"))
        except:
            return None
        return response


class APIVoiceClient(object):
    url = getattr(settings, "NETELIP_API_URL", "https://apivoice.netelip.com")
    api = getattr(settings, "NETELIP_API_NAME", "API 31c06")
    token = getattr(settings, "NETELIP_API_TOKEN", "9837689aa6feda2c3d8b0b6c6e8c94bb896fbaf8505f9c346a81c68248e36a6f")
    duration = 60

    def _api_call(self, dst, typedst, src=None, duration=None, userdata=None):
        data = {
            'api': self.api,
            'token': self.token,
            'src': src,
            'dst': dst,
            'typedst': typedst,
            'duration': duration or self.duration,
            'userdata': userdata or "",
        }
        response = requests.post(url=self.url, data=data)
        if ((response.status_code == status.HTTP_200_OK) and
                (json.loads(response.content).get("response") == str(status.HTTP_200_OK))):
            return response
        else:
            raise Exception(_("Something wrong happens with Netelip call. Please, try again later."))

    def internal_c2c(self, flow_id, first_step, phone_orig, type_phone_orig, phone_dest, src=None, duration=None):
        extra_data = json.dumps("%s;%s;%s;%s;%s" % (flow_id, "", first_step, phone_orig, phone_dest))
        return self._api_call(dst=phone_orig, typedst=type_phone_orig, src=src,
                              duration=duration, userdata=extra_data)


class CallProcess(object):
    called = None               # Called phone/extension/s (extensions separated by "&". Example: ext1&ext&est3)
    caller = None               # Caller phone
    next_step = None            # Next Step - Command instance
    current_step = None         # Current Step - Command instance
    src = None                  # Mask to show (must be one Netelip Number)
    dtmf = None                 # Digit marked - Flow Way
    flow = None                 # Flow instance
    dst = None


    def set_flow(self, id):
        try:
            self.flow = Flow.objects.get(id=id)
        except Flow.DoesNotExist:
            self.flow = None

    def set_current_step(self, id):
        try:
            self.current_step = Command.objects.get(id=id)
        except (Command.DoesNotExist, ValueError):
            self.current_step = None

    def set_next_step(self, id_list):
        query = {'id__in': id_list}
        query.update({'dtmf': self.dtmf}) if self.dtmf else None
        try:
            self.next_step = Command.objects.get(**query)
        except (Command.DoesNotExist, ValueError):
            self.next_step = None

    def get_userfield(self, data):
        userfield_data = data.get("userfield", "") or data.get("userdata", "")
        userfield_data = userfield_data.split(";")
        return userfield_data

    def process_userfield(self, userfield_data):
        if len(userfield_data) == 5:
            self.set_flow(id=userfield_data[0])
            self.set_current_step(id=userfield_data[1])
            self.set_next_step(id_list=userfield_data[2].split("&"))
            self.caller = userfield_data[3]
            self.called = userfield_data[4]

    def process_data(self, data):
        src = data.get('src')
        dst = data.get('dst')
        self.src = src
        self.dst = dst
        self.dtmf = data.get('dtmf')
        self.process_userfield(self.get_userfield(data))

    def run_validators(self, data):
        validator = None
        result = True
        if self.current_step and self.current_step.command:
            validator = getattr(self, "validate_%s" % self.current_step.command, None)
        if validator:
            result = validator(data)
        return result

    def get_step(self, command_instance):
        options_kwargs = {
            'called': self.called, 'caller': self.caller, 'next_step': self.next_step,
            'current_step': self.current_step, 'src': self.src, 'dtmf': self.dtmf,
            'flow': self.flow, 'dst': self.dst
        }
        command_instance = command_instance or self.flow.command_set.get(is_error=True)
        step = {
            "command": command_instance.command, "options": command_instance.get_options(options_kwargs),
            "userfield": command_instance.user_field(self.caller, self.called)
        }
        return step

    def get_operation(self, data):
        self.process_data(data)
        step = self.get_step(self.next_step)
        current_step = self.get_step(self.current_step)
        final_step = step if self.run_validators(data) else current_step
        return final_step
