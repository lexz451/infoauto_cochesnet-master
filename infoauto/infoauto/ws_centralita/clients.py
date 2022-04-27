# coding: utf-8
import datetime
import urllib.parse

import requests
from django.conf import settings
from rest_framework import status


class ClientWSCentralita(object):
    def __init__(self, url=None, id_cliente=None, token=None):
        self.url = url or getattr(settings, 'URL_WS_CENTRALITA', 'https://wscentralita.premiumnumbers.es/WSCentralita/')
        self.id_cliente = id_cliente or getattr(settings, 'ID_CLIENTE_WS_CENTRALITA', 22520)
        self.token = token or getattr(settings, 'TOKEN_WS_CENTRALITA', "hh7drKYYHjyUsDUJhrsx")

    @staticmethod
    def validate_date(date_text, param_name):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d %h:%m:%s')
        except ValueError:
            raise ValueError("Formato de '%s' incorrecto, debería ser AAAA-MM-DD hh:mm:ss" % param_name)

    @staticmethod
    def validate_reg_num(reg_num):
        if reg_num > 500:
            raise ValueError("El número de registros no puede ser superior a 500")

    def _parse_data_url(self, api_format="json", method=None, extra_data=None):
        extra_data = extra_data or {}
        base_url = self.url.rstrip('/') if self.url.endswith('/') else self.url
        credentials = {'idCliente': self.id_cliente, 'token': self.token}
        path = urllib.parse.urlencode({**credentials, **extra_data})
        url = "%(base_url)s/%(api_format)s/%(method)s/%(path)s" % {'base_url': base_url, 'api_format': api_format,
                                                                   'method': method, 'path': path}
        return url

    def call(self, http_method='get', api_format="json", method=None, extra_data=None):
        url = self._parse_data_url(api_format=api_format, method=method, extra_data=extra_data)
        max_attempts = getattr(settings, 'MAX_ATTEMPTS', 5)
        attempt = 0
        allowed_status = [status.HTTP_200_OK, status.HTTP_201_CREATED]
        response = None
        while not response or (response.status_code not in allowed_status) or (attempt <= max_attempts):
            response = getattr(requests, http_method, 'get')(url=url)
            attempt += 1
            # sleep(2)  # Time between attempts
        return response

    def get_datos_cliente(self, api_format='json'):
        return self.call(method='GetDatosCliente', api_format=api_format)

    def get_info_extensiones(self, api_format='json'):
        return self.call(method='GetInfoExtensiones', api_format=api_format)

    def get_llamadas_en_curso(self, api_format='json'):
        return self.call(method='GetLLamadasEnCurso', api_format=api_format)

    def get_agenda(self, api_format='json'):
        return self.call(method='GetAgenda', api_format=api_format)

    def get_estadisticas_cliente_fecha_hora_inicio(
            self, api_format='json', fecha_hora_inicio=None, numero_registros=500):
        self.validate_reg_num(numero_registros)
        self.validate_date(fecha_hora_inicio, param_name='fechaHoraInicio')
        extra_data = {'fechaHoraInicio': fecha_hora_inicio, 'numeroRegistros': numero_registros}
        return self.call(method='GetEstadisticasClienteFechaHoraInicio',
                         api_format=api_format, extra_data=extra_data)

    def get_estadisticas_cliente_fecha_hora_inicio_con_segmentos(
            self, api_format='json', fecha_hora_inicio=None, numero_registros=500):
        self.validate_reg_num(numero_registros)
        self.validate_date(fecha_hora_inicio, param_name='fechaHoraInicio')
        extra_data = {'fechaHoraInicio': fecha_hora_inicio, 'numeroRegistros': numero_registros}
        return self.call(method='GetEstadisticasClienteFechaHoraInicioConSegmentos',
                         api_format=api_format, extra_data=extra_data)

    def get_estadisticas_cliente_ultimo_id(self, api_format='json', id_llamada_inicio=None, numero_registros=500):
        self.validate_reg_num(numero_registros)
        extra_data = {'idLlamadaInicio': id_llamada_inicio, 'numeroRegistros': numero_registros}
        return self.call(method='GetEstadisticasClienteUltimoId',
                         api_format=api_format, extra_data=extra_data)

    def get_estadisticas_cliente_ultimo_id_con_seguimientos(
            self, api_format='json', id_llamada_inicio=None, numero_registros=500):
        self.validate_reg_num(numero_registros)
        extra_data = {'idLlamadaInicio': id_llamada_inicio, 'numeroRegistros': numero_registros}
        return self.call(method='GetEstadisticasClienteUltimoIdConSegmentos',
                         api_format=api_format, extra_data=extra_data)

    def get_grabacion_llamada(self, api_format='json', extra_data=None):
        return self.call(method='GetGrabacionLlamada',
                         api_format=api_format, extra_data=extra_data)

    def get_grabacion_llamada_id_original(self, api_format='json', extra_data=None):
        return self.call(method='GetGrabacionLlamadaIdOriginal',
                         api_format=api_format, extra_data=extra_data)
