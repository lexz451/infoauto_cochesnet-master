import requests
from bs4 import BeautifulSoup
from django.conf import settings

from infoauto.netelip.models import SMSMessages

NetelipSMSErrorCodes = {
    103: "Early Hints -- Parámetros erroneos",
    200: "OK -- Petición realizada correctamente",
    401: "Unauthorized -- Error de autentificación, compruebe token",
    402: "Payment required -- Saldo insuficiente para el envío sms",
    404: "Not Found -- No encontrado ID del sms enviado",
    406: "Not Acceptable -- Parámetro obligatorio omitido",
    412: "Precondition failed -- Error no reconocido",
    500: "Internal Server Error -- Hemos tenido problema con nuestros servidores, intentelo de nuevo",
    503: "Service Unavailable -- El servicio está temporalmente en mantenimiento. Por favor intentelo más tarde."
}

class NetelipSMSException(Exception):
    pass


class NetelipSMS:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def send(self, from_sms, destination_sms, message_sms):
        data = {
            'token': self.token,
            'from': from_sms,
            'destination': destination_sms,
            'message': message_sms
        }

        response = requests.post(url=self.url, data=data)

        if response and response.status_code == 200:
            try:
                xml = BeautifulSoup(response.text, 'html.parser')
                status = xml.response.status.text
                id_sms = getattr(xml.response, "id-sms").text
            except Exception:
                raise NetelipSMSException("Formato respuesta Netelip SMS incorrecto", response.text)
        else:
            raise NetelipSMSException(response.status_code, NetelipSMSErrorCodes[response.status_code])

        return {
            "status": status,
            "id_sms": id_sms,
            "from_sms": from_sms,
            "destination_sms": destination_sms,
            "message": message_sms
        }


def send_sms(from_sms, destination_sms, message_sms):
    pass
    # if from_sms and destination_sms:
    #     netelip_sms_client = NetelipSMS(token=settings.NETELIP_SMS_APITOKEN, url=settings.NETELIP_SMS_URL)
    #     result = netelip_sms_client.send(from_sms.replace('+', '00'), destination_sms.replace('+', '00'), message_sms)
    #     SMSMessages.objects.create(**result)
