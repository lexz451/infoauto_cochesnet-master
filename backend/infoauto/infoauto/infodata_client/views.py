from rest_framework.parsers import FormParser
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet

from infoauto.infodata_client.serializers import InfodataSerializer
from infoauto.leads.models import ACD


xml_response_base = """
<?xml version="1.0" encoding="UTF-8"?>
<ROOT>
    <STATUS>
        <STATUS_CODE>OK</STATUS_CODE>
        <STATUS_DESC>New resource created</STATUS_DESC>
    </STATUS>
</ROOT>
"""


class InfodataIncomingCallView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = InfodataSerializer
    queryset = ACD.objects.all()
    parser_classes = (FormParser, )

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            self.serializer_class = InfodataSerializer
        return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        """Script allowing connection with Zadarma"""
        return HttpResponse(xml_response_base)

    def create(self, request, *args, **kwargs):
        """
        tipo =  es simplemente para indicar que tipo de petición se hace, para este caso tendrá el literal "finllamada"
        origen = es el numero origen de llamada
        sesion = es un identificativo único de la llamada, que tiene el siguiente formato "2161458296071.9052"
        servicio = es el numero destino de llamada
        agente = es el código del agente que atiende la llamada
        fecha = '2016/04/26 13:35:45'
        grabacion = (url de la grabación)
        duración = (en segundos)
        estado = (0 – no atendida, 1 – atendida)
        """

        with open("/tmp/telefono.txt", "w+") as file:
            file.write(str(request.data))
        return HttpResponse(xml_response_base)

"""
response = super().create(request, *args, **kwargs)
if response.status_code == status.HTTP_201_CREATED:
    return HttpResponse(xml_response_base)
else:
    return response
"""

