# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CharField, TextField, PositiveSmallIntegerField, ForeignKey, BooleanField, SlugField, \
    ManyToManyField
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from infoauto.common.util_phone import normalize_phone
from infoauto.netelip.validators import validate_nonzero
from infoauto.taskapp.celery import check_all_incoming_calls_is_duplicated

STATUSCALL_CHOICES = (
    ('CHANUNAVAIL', _('El número llamado no existe')),
    ('BUSY', _('El número llamado está ocupado')),
    ('NOANSWER', _('El número llamado no contesta')),
    ('ANSWER', _('El número llamado ha contestado')),
    ('CANCEL', _('El número llamado ha colgado')),
    ('CONGESTION', _('Fallo en red telefónica por congestión')),
    ('UNKNOW', _('Fallo en red telefónica desconocido'))
)

TYPESRC_CHOICES = (
    ('ext', _('llamada con origen una extensión de tu vPBX cuando ésta tiene el asociado el '
              '"Plan de marcado de API Voice"')),
    ('did', _('llamada con destino un número de teléfono de netelip gestionado por API Voice'))
)


CALL_ORIGIN_CHOICES = (
    ('user', _("Usuario")),
    ('client', _("Client"))
)

SIMPLE_STATUS_CHOICES = (
    ('communicate', _('Llamada entrante')),
    ('no_answer', _('No respondida')),
    ('answer', _('Respondida')),
    ('end', _('Finalizada')),
)


class CallControlModelHistoricalRecords(HistoricalRecords):
    pass


class CallControlModel(TimeStampedModel):
    id_call = models.FloatField(unique=True, help_text=_("ID único de la llamada"))
    api = models.CharField(max_length=255, help_text=_("Nombre del API destino de la llamada"))
    src = models.CharField(max_length=255, help_text=_("Número de origen de la llamada"))
    dst = models.CharField(max_length=255, help_text=_("Número de destino de la llamada"))
    startcall = models.DateTimeField(help_text=_("Fecha y hora en la que comenzó la llamada"))
    durationcall = models.DurationField(help_text=_("Duración actual de la llamada"), blank=True, null=True)
    durationcallanswered = models.DurationField(help_text=_("Duración de la llamada una vez atendida por un agente"),
                                                blank=True, null=True)
    command = models.CharField(max_length=255, help_text=_("Comando ejecutado"), blank=True, null=True)
    options = models.TextField(help_text=_("Opciones del comando ejecutado"), blank=True, null=True)
    description = models.TextField(help_text=_("Descripción del resultado de la ejecución del comando"),
                                   blank=True, null=True)
    dtmf = models.CharField(help_text=_("Dígito DTMF - Dígito marcado en la llamada para establecer flujo"),
                            blank=True, null=True, max_length=255)
    statuscode = models.IntegerField(help_text=_("Código de estado de la ejecución"), blank=True, null=True)
    statuscall = models.CharField(max_length=255, choices=STATUSCALL_CHOICES, help_text=_("Estado de la llamada"),
                                  blank=True, null=True)
    userdata = models.CharField(max_length=255, help_text=_("Variable establecida por el usuario"),
                                blank=True, null=True)
    typesrc = models.CharField(choices=TYPESRC_CHOICES, max_length=255, help_text=_("Tipo de origen"),
                               blank=True, null=True)
    usersrc = models.CharField(help_text=_("Usuario del origen de la llamada. Cuando el tipo de origen es 'ext', "
                                           "el valor de 'usersrc' será el usuario SIP de la extensión que realiza la "
                                           "llamada;"
                                           "Cuando el tipo de origen es 'did', será el número de teléfono de origen "
                                           "de la llamada, tendrá el mismo valor que 'src'."),
                               max_length=255, blank=True, null=True)

    # Project attributes
    call_origin = models.CharField(help_text=_("Origen de la llamada"), choices=CALL_ORIGIN_CHOICES,
                                   max_length=255, blank=True, null=True)

    startcall_time = models.TimeField(blank=True, null=True)

    history = CallControlModelHistoricalRecords()
    is_checked = BooleanField(default=False)

    ubunet_company = models.CharField(help_text=_("Company en ubunet"), max_length=255, null=True, default=None)
    ubunet_extension = models.CharField(help_text=_("Extension en ubunet"), max_length=255, null=True, default=None)
    ubunet_agent = models.CharField(help_text=_("Agente en ubunet"), max_length=255, null=True, default=None)
    ubunet_audio_downloaded = BooleanField(default=False)
    ubunet_holdtime = models.DurationField(help_text=_("Duración en espera"), null=True, default=None)

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        if self.startcall:
            self.startcall_time = self.startcall.time()

        self.src = normalize_phone(self.src)
        self.dst = normalize_phone(self.dst)

        if is_new and self.call_origin == 'client':
            check_all_incoming_calls_is_duplicated.apply_async(countdown=10)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Llamada entrante/saliente")
        verbose_name_plural = _("Llamadas entrantes/salientes")


    # Función de cálculo del estado real de la llamadas, implementado por @adam.
    # por petición expresa de Susana, cambiamos esto a la siguiente función.
    #
    # @property
    # def simple_status(self):
    #     option = 'communicate'
    #     options = dict(SIMPLE_STATUS_CHOICES)
    #     queryset = self.history.filter(command='dial')
    #     if queryset.exists():
    #         option = 'no_answer' if queryset.count() == 1 else 'answer'
    #     return options[option]

    @property
    def has_audio(self):
        return self.ubunet_audio_downloaded
        # if self.description.startswith("/APIVoice/Record/"):
        #     return True
        # if [i for i in self.history.all().values_list('description', flat=True) if i and i.startswith("/APIVoice/Record/")]:
        #     return True
        # return False

    @property
    def simple_status(self):
        # Susana pide mostrar el campo statuscall.
        return self.statuscall


COMMAND_CHOICES = (
    ('hangup', 'hangup: Cuelga la llamada en curso'),
    ('busy', "busy: Dar señal de ocupado en la llamada actual. Valor de 0 a 30. Por defecto 30 segundos."),
    ('congestion', "congestion: Dar señal de congestión en la red en la llamada actual. Valor de 0 a 30. Por defecto 30 segundos."),
    ('play', "play: Reproduce sonido guardado en vPBX (tipo de localización 'local') o en servidor web remoto "
             "(tipo de localización 'remote'). Se pueden reproducir varios fcheros de forma secuencial poniendo "
             "como separador entre fcheros '&' (solo disponible para localización 'local')"),
    ('language', "language: Establece el idioma para las locuciones predeterminadas cuando una llamada se desvía a vPBX, como "
                 "puede ser 'Por favor deje su mensaje después de la señal'. Por defecto el idioma es el inglés (en)."),
    ('speak', "speak: Reproduce el texto con la voz que se especifca (Text to speech). Importante: La velocidad de "
              "reproducción de la voz solo aplica a google pudiendo ser 1, la más lenta, hasta 2 la más rápida."),
    ('voicemail', "voicemail: Deja un mensaje en el buzón de voz de una o varias extensiones de vPBX. "
                  "Si se añade varias extensiones, estas deben ir separadas por '&'."),
    ('queue', "queue: Transfere una llamada a una cola de llamadas existente en vPBX con o sin prioridad."),
    ('play_getdtmf', "play_getdtmf: Reproduce un fchero de audio guardado en vPBX (tipo de localización 'local') o en servidor web "
                     "remoto (tipo de localización 'remote') esperando a que sea marcada una opción por DTMF."),
    ('ivr', "ivr: Transfere una llamada a un IVR existente en vPBX."),
    ('conferenceroom', "conferenceroom: Transfere la llamada a su sala de conferencias de vPBX."),
    ('speak_getdtmf', "speak_getdtmf: Reproduce un texto con la voz que se especifica (Text to speech) esperando a que sea marcada "
                      "una opción. Importante: La velocidad de reproducción de la voz solo aplica a google pudiendo "
                      "ser 1, la más lenta, hasta 2 la más rápida."),
    ('record', "record: Inicia la grabación de la llamada y finalizará cuando finalice la llamada."),
    ('callerid', "callerid: Cambia el identificador llamada en previo a un desvío o transferencia."),
    ('dial', "dial: Hace una llamada a un destino, ya sea extensión de vPBX, teléfono de la red pública o extensión de un "
             "servidor SIP."),
    ('google_voice2text', "google_voice2text: Se utiliza el servicio de reconocimiento de voz de google para convertir la voz del llamante "
                          "o llamado en texto legible por la aplicación del cliente."),
    ('send_dtmf', "send_dtmf: Genera tonos DTMF en la llamada en curso."),
)

COMMAND_OPTIONS = {
    'hangup': None,
    'busy': {
        'duracion_tonos': "Duración en segundos de los tonos de ocupado antes descolgar.",
        "_format": "%(duracion_tonos)s"
    },
    'congestion': {
        'duracion_tonos': "Duración en segundos de los tonos de congestión antes de colgar.",
        "_format": "%(duracion_tonos)s"
    },
    'play': {
        'localizacion': "Tipo de localización: 'local' o 'remote'",
        'ficheros': "Nombre/s de fichero/s de audio sin extensión.",
        "_format": "%(localizacion)s;%(ficheros)s"
    },
    'language': {
        'lang': "'es' (Español) o 'en' (Inglés)",
        '_format': "%(lang)s"
    },
    'speak': {
        'proveedor': "'netelip' o 'google'",
        'codigo': "Tabla de idiomas TTS",
        'texto_a_reproducir': "Texto a reproducir",
        'velocidad_reproduccion': "Velocidad de reproducción. Valor de 1 a 2 (ejemplo, 1.2).",
        '_format': "%(proveedor)s;%(codigo)s;%(texto_a_reproducir)s;%(velocidad_reproduccion)s"
    },
    'voicemail': {
        'extension': "",
        '_format': "%(extension)s"
    },
    'queue': {
        'nombre_de_cola': "Nombre de la cola.",
        'prioridad': "Prioridad. Prioridad que se le da a la llamada dentro de la cola. Valor entre 1 y 10, "
                     "siendo 1 la máxima prioridad. Por defecto valor 0, siendo encolada cada llamada por orden de "
                     "entrada (modo FIFO).",
        '_format': "%(nombre_de_cola)s,%(prioridad)s",
    },
    'play_getdtmf': {
        'local': "Tipo de localización: 'local' o 'remote'",
        'fchero_de_audio': "Nombre/s de fichero/s de audio sin extensión.",
        'tiempo_de_espera': "Tiempo de espera (en milisegundos)",
        'max_digitos_dtmf': "Máximo de dígitos DTMF",
        '_format': "%(local)s;%(fchero_de_audio)s;%(tiempo_de_espera)s;%(max_digitos_dtmf)s"
    },
    'ivr': {
        'nombre_IVR': "Nombre del IVR en vPBX",
        '_format': "%(nombre_IVR)s"
    },
    'conferenceroom': None,
    'speak_getdtmf': {
        'proveedor': "Proveedor: 'netelip' o 'google'.",
        'voz_o_idioma': "Código: Tabla de idiomas TTS.",
        'texto_a_reproducir': "Texto a reproducir.",
        'tiempo_de_espera': "Tiempo de espera (en milisegundos)",
        'max_digitos_dtmf': "Máximo de dígitos DTMF",
        'velocidad_reproduccion': "Velocidad de reproducción. Valor de 1 a 2 (ejemplo, 1.2)",
        '_format': "%(proveedor)s;%(voz_o_idioma)s;%(texto_a_reproducir)s;%(tiempo_de_espera)s;%(max_digitos_dtmf)s;%(velocidad_reproduccion)"
    },
    'record': None,
    'callerid': {
        'nombre': "Nombre a mostrar",
        'n_telefono': "Número de teléfono a mostrar",
        '_format': "%(nombre)s;%(n_telefono)s"
    },
    'dial': {
        'tipo': "'extension' (La llamada se hace a una/s extensión/es de vPBX), "
                "'pstn' (La llamada se hace a un número de teléfono de la red telefónica pública.) "
                "'sipserver' (La llamada se hace un servidor SIP, indicando extensión, ip y puerto del servidor SIP de destino.)",
        'n_telefono': "número de telefono, extensión o sipserver (ej: 2000@8.8.8.8:5060)",
        'max_duracion_ring': "Duración del ring de 1 a 60",
        'calling_or_called': "'calling': Permite al usuario llamante transferir la llamada pulsando '#'. "
                             "'called': Permite al usuario llamado transferir la llamada pulsando '#'.",
        'timeout': "Permite al usuario establecer la duración máxima de conversación en la llamada, "
                   "siendo el valor mínimo de 5 segundos y máximo de 10 horas (36000 segundos) "
                   "(opcional, valor en segundos)",
        '_format': "%(pstn)s,%(n_telefono)s,%(max_duracion_ring)s,%(calling_or_called)s,%(timeout)s",
    },
    'google_voice2text': {
        'key': "generada en la API de reconocimiento de voz de Google APIs.",
        'idioma': "Código del idioma a reconocer de la 'Tabla de idiomas de reconocimiento de voz'.",
        'tiempo_de_espera': "nº de segundos de silencio que espera detectar hasta mandar la petición a Google",
        'beep': "reproducir el sonido 'beep' para indicar el comienzo de la escucha.",
        '_format': "%(key)s;%(idioma)s;%(tiempo_de_espera)s;%(beep)s"
    },
    'send_dtmf': {
        'digitos': "lista de dígitos, comprendidos entre 0-9, a-d, A-D,#,*",
        'timeout': "duración en segundos entre tono y tono. Valores comprendidos entre 1-60.",
        '_format': "%(digitos)s;%(timeout)s"
    }
}


TYPE_FLOW_CHOICES = (
    ('c2c', _("Click2Call")),
    ('flow', _("Flujo"))
)


class Flow(TimeStampedModel):
    type = CharField(choices=TYPE_FLOW_CHOICES, default='flow', max_length=255)
    is_default = BooleanField(default=False)

    allowed = BooleanField(default=True)
    name = CharField(max_length=255)
    slug = SlugField(editable=False, blank=True, null=True)
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Flow")
        verbose_name_plural = _("Flows")


class Command(TimeStampedModel):
    is_initial = BooleanField(default=False)
    is_error = BooleanField(default=False)

    flow = ForeignKey(Flow, on_delete=models.CASCADE)
    dtmf = CharField(blank=True, null=True, max_length=255)
    prev_commands = ManyToManyField('self', related_name="next_commands", blank=True, symmetrical=False)
    command = CharField(max_length=255, choices=COMMAND_CHOICES)
    options = TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Command")
        verbose_name_plural = _("Commands")

    def user_field(self, caller, called, first_execution=False):
        if first_execution:
            current_step = ''
            next_step = self.id
        else:
            current_step = self.id
            next_command = self.next_commands.all()
            next_step = "&".join(map(str, next_command.values_list("id", flat=True)))
        user_field = "%(flow_id)s;%(current_step)s;%(next_step)s;%(caller)s;%(called)s" % {
            'current_step': current_step, 'flow_id': self.flow.id, "caller": caller, "called": called,
            'next_step': next_step
        }
        return user_field

    def get_options(self, kwargs):
        """
        :param kwargs:
            called = Called phone/extension/s (extensions separated by "&". Example: ext1&ext&est3)
            caller = Caller phone
            next_step = Next Step - Command instance
            current_step = Current Step - Command instance
            src = Mask to show (must be one Netelip Number)
            dtmf = Digit marked - Flow Way
            flow = Flow instance
        :return:
        """

        return self.options % kwargs


class SMSMessages(TimeStampedModel):
    id_sms = CharField(max_length=255)
    from_sms = CharField(max_length=255)
    destination_sms = CharField(max_length=255)
    message = TextField()
    status = PositiveSmallIntegerField()

