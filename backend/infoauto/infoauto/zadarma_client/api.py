# -*- coding: utf-8 -*-

import hmac
import requests
import base64

from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from hashlib import sha1, md5
from urllib.parse import urlencode


class ZadarmaAPI(object):

    def __init__(self, key, secret, is_sandbox=False):
        """
        Constructor
        :param key: key from personal
        :param secret: secret from personal
        :param is_sandbox: (True|False)
        """
        self.key = key
        self.secret = secret
        self.is_sandbox = is_sandbox
        self.__url_api = 'https://api.zadarma.com'
        if is_sandbox:
            self.__url_api = 'https://api-sandbox.zadarma.com'

    def call(self, method, params=None, request_type='GET', format='json', is_auth=True):
        """
        Function for send API request
        :param method: API method, including version number
        :param params: Query params
        :param request_type: (get|post|put|delete)
        :param format: (json|xml)
        :param is_auth: (True|False)
        :return: response
        """
        params = params or {}
        request_type = request_type.upper()
        allowed_type = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if request_type not in allowed_type:
            # request_type = 'GET'
            raise ValueError(_("El método especificado no es correcto"))
        params['format'] = format
        auth_str = None
        if is_auth:
            auth_str = self.__get_auth_string_for_header(method, params)

        result = False
        if request_type == 'GET':
            sorted_dict_params = OrderedDict(sorted(params.items()))
            params_string = urlencode(sorted_dict_params)
            request_url = self.__url_api + method + '?' + params_string
        else:
            request_url = self.__url_api + method
        result = getattr(requests, request_type.lower())(request_url, headers={'Authorization': auth_str}, data=params)
        return result.text

    def __get_auth_string_for_header(self, method, params):
        """
        :param method: API method, including version number
        :param params: Query params dict
        :return: auth header
        """
        sorted_dict_params = OrderedDict(sorted(params.items()))
        params_string = urlencode(sorted_dict_params)
        md5hash = md5(params_string.encode('utf8')).hexdigest()
        data = method + params_string + md5hash
        hmac_h = hmac.new(self.secret.encode('utf8'), data.encode('utf8'), sha1)
        bts = bytes(hmac_h.hexdigest(), 'utf8')
        auth = self.key + ':' + base64.b64encode(bts).decode()
        return auth
