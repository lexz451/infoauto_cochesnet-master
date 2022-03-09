from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.fields import CharField, BooleanField, IntegerField, ChoiceField, DateTimeField

from infoauto.leads.models import Client


class Extensiones(serializers.Serializer):
    numero = CharField(help_text="número de teléfono de la extensión")
    enHorario = BooleanField(help_text="indica si la extensión está en horario en ese momento")
    ocupado = BooleanField(help_text="indica si la extensión está ocupada")
    logueado = BooleanField(help_text="indica si la extensión está logueada en la Centralita Virtual")
    ip = BooleanField(help_text="indica si la extensión es IP")
    direccionIP = CharField(help_text="indica la IP si la extensión es IP. En caso contrario está en blanco")
    latencia = IntegerField(help_text="indica la latencia, en milisegundos, si la extensión es IP (por defecto 0)")
    registrado = BooleanField(help_text="indica la latencia, en milisegundos, si la extensión es IP (por defecto 0)")


class Llamadas(serializers.Serializer):
    tipo = ChoiceField(choices=("Entrante", "Saliente", "Interna"),
                       help_text="tres valores posibles: “Entrante”, “Saliente” o “Interna”")
    duracion = IntegerField(help_text="duración de la llamada en tiempo real")
    encaminamiento = CharField(help_text="encaminamiento por el que ha entrado la llamada")
    estado = ChoiceField(
        choices=("Finalizada", "Locución", "En cola", "En enrutamiento", "Conectada"),
        help_text="varios valores posibles: Finalizada, Locución, En cola, En enrutamiento y Conectada."
                  " Las llamadas finalizadas se incluyen solo si han finalizado en los últimos minutos.")
    fechaHoraInicio = DateTimeField(format="%d/%m/%Y %h:%m:%s",
                                    help_text="fecha y hora de inicio de la llamada (dd/mm/aaaa hh:mm:ss)")
    numeroDestino = CharField(help_text="número del destino que ha descolgado la llamada. Si no ha "
                                        "descolgado nadie el campo estará en blanco")
    nombreDestino = CharField(help_text="nombre del destino. Si la llamada es saliente y el destino está "
                                        "guardado en la agenda mostrará el nombre del contacto")
    numeroOrigen = CharField(help_text="número del llamante")
    nombreOrigen = CharField(help_text="nombre del llamante en caso de estar en la agenda del cliente")
    numeroOriginal = CharField(help_text="número al que ha llamado el llamante")


class Agenda(serializers.Serializer):
    id = IntegerField(help_text="identificador único del contacto, necesario para editarlo y eliminarlo más tarde.")
    idCliente = IntegerField(help_text="idCliente en el que está creado el contacto")
    nombre = CharField(help_text="nombre dado al contacto y que aparecerá en las llamadas "
                                 "salientes/entrantes a/de dicho contacto")
    telefono = CharField(help_text="teléfono del contacto")
    telefono2 = CharField(help_text="teléfono alternativo 2")
    telefono3 = CharField(help_text="teléfono alternativo 3")
    fax = CharField(help_text="número de fax")
    correo = CharField(help_text="dirección de correo electrónico")
    comentario = CharField(help_text="notas que el cliente ha escrito para identificar al contacto")


class Cliente(WritableNestedModelSerializer):
    Extensiones = Extensiones(many=True, write_only=True)
    Llamadas = Llamadas(many=True, write_only=True)
    Agenda = Agenda(many=True, write_only=True)

    class Meta:
        model = Client
        fields = ("Extensiones", "Llamadas", "Agenda")


class LlamadasEstadisticas(serializers.Serializer):
    idLlamada = IntegerField(help_text="identificador interno de la llamada. Sirve para obtener las siguientes"
                                       "llamadas con GetEstadisticasClienteUltimoId, o para obtener la grabación con"
                                       "GetGrabacionLlamada")
