from rest_framework import serializers

from infoauto.leads.models import ACD


class InfodataSerializer(serializers.ModelSerializer):
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
    tipo = serializers.CharField()
    origen = serializers.CharField()
    sesion = serializers.CharField(source='acd_id')
    servicio = serializers.CharField(source='lead_phone')
    agente = serializers.CharField()
    fecha = serializers.CharField(source='acd_date')
    grabacion = serializers.CharField(source='acd_audio_link')
    duracion = serializers.CharField()
    estado = serializers.IntegerField()

    class Meta:
        fields = ('id', 'tipo', 'origen', 'sesion', 'servicio', 'agente', 'fecha', 'grabacion', 'duracion', 'estado')
        model = ACD
        read_only_fields = ('id', )
