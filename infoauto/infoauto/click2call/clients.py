import requests
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from django.conf import settings


class Client(object):

    def __init__(self, auth=None, headers=None, url=None, *args, **kwargs):
        self.url = url or getattr(settings, 'URL_CLICK_2_CALL', "https://www.panelcliente.com/c2c/ws.php")
        self.service_kwargs = {'auth': auth, 'headers': headers, 'url': url or self.url, **kwargs}
        self.data = kwargs.get('data', {})

    def get(self):
        raise NotImplementedError()

    def post(self, *args, **kwargs):
        """
        Sends a POST request
        :param accion: (optional) Service to call
        :param idcliente: (optional) Authentication identifier for service
        :param memberid: (optional) concession member to call
        :param telefono: (optional) client phone to call
        :return: Dictionary
        """
        data = getattr(settings, 'CLICK_2_CALL', {
            "accion": "solicitar", "idcliente": "15", "memberid": "", "telefono": ""
        })
        data = {**data, **self.data, **kwargs}
        response = requests.post(data=data, **self.service_kwargs)
        return self._parse_response(response)

    def _parse_response(self, response):
        """
        Parse resp
        :param response: class:`Response <Response>` object
        :return: dict: Dictionary
        """
        if response.content == b'OK.Le estamos llamando. Por favor, espere.':
            return {'status': True, 'status_code': response.status_code, 'message': response.content}
        else:
            return {'status': False, 'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': response.content or _("Service connection failure")}
