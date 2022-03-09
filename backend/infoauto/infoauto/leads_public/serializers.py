import drf_writable_nested

from rest_framework import serializers

from infoauto.leads.models import Lead, Vehicle, Origin, Task, Request, Note


class WritableNestedModelSerializer(drf_writable_nested.WritableNestedModelSerializer):
    @staticmethod
    def void_value(*args, **kwargs):
        return None


class PublicVehicleSerializer(WritableNestedModelSerializer):
    marca = serializers.CharField(source='brand_model')
    modelo = serializers.SerializerMethodField(method_name='void_value')
    precio = serializers.CharField(source='price')
    combustible = serializers.SerializerMethodField()
    financiaria = serializers.SerializerMethodField(method_name='void_value')
    rangos = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ('marca', 'modelo', 'precio', 'combustible', 'financiaria', 'rangos')
        extra_kwargs = {'gas': {'write_only': True}}

    def get_rangos(self, obj):
        return {'anio': {'desde': obj.year, 'hasta': obj.year},
                'precio': {'desde': obj.price, 'hasta': obj.price},
                'kilometros': {'desde': obj.km, 'hasta': obj.km}}

    def get_combustible(self, obj):
        return obj.gas.name if obj.gas else None


class PublicOriginSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Origin
        fields = ('id', 'name', 'icon')


class FilteredTaskListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        """
        TODO: Not update implemented. View how to. Abstract method
        :param instance:
        :param validated_data:
        :return: list of instances
        """
        pass

    def to_representation(self, data):
        data = data.filter(appraisal__isnull=False)
        return super().to_representation(data)


class PublicTaskSerializer(WritableNestedModelSerializer):
    tipovehiculo = serializers.SerializerMethodField(method_name='void_value')
    marca = serializers.CharField(source='appraisal.brand_model')
    modelo = serializers.SerializerMethodField(method_name='void_value')
    cambio = serializers.SerializerMethodField(method_name='void_value')
    version = serializers.SerializerMethodField(method_name='void_value')
    km = serializers.CharField(source='appraisal.km')
    cv = serializers.SerializerMethodField(method_name='void_value')
    cilindrada = serializers.SerializerMethodField(method_name='void_value')
    matricula = serializers.CharField(source='appraisal.license_plate')
    fechaprimeramatriculacion = serializers.SerializerMethodField()
    combustible = serializers.SerializerMethodField()
    preciodeseado = serializers.SerializerMethodField(method_name='void_value')

    class Meta:
        list_serializer_class = FilteredTaskListSerializer
        model = Task
        fields = ('tipovehiculo', 'marca', 'modelo', 'cambio', 'version', 'km', 'cv', 'cilindrada', 'matricula',
                  'fechaprimeramatriculacion', 'combustible', 'preciodeseado')

    def get_fechaprimeramatriculacion(self, obj):
        return {'anio': obj.appraisal.year, 'mes': obj.appraisal.year, 'dia': obj.appraisal.year}

    def get_combustible(self, obj):
        return obj.appraisal.gas.name if obj.appraisal.gas else None


class PublicNoteSerializer(WritableNestedModelSerializer):
    fechahora = serializers.DateTimeField(source='created')
    comentario = serializers.CharField(source='content')
    recordarenfecha = serializers.SerializerMethodField(method_name='void_value')

    class Meta:
        model = Note
        fields = ('fechahora', 'comentario', 'recordarenfecha')


class PublicLeadSerializer(WritableNestedModelSerializer):
    identificador = serializers.PrimaryKeyRelatedField(source='id', queryset=Lead.objects.all())
    fechaalta = serializers.SerializerMethodField()
    horaalta = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()
    apellidos = serializers.SerializerMethodField(method_name='void_value')
    telefono = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    origen = serializers.SerializerMethodField()
    soloventa = serializers.SerializerMethodField(method_name='void_value')
    tasacion = serializers.SerializerMethodField()
    score = serializers.CharField(source="get_score_display")
    estado = serializers.CharField(source='get_status_display')
    resultado = serializers.CharField(source='get_result_display')
    concesiondestino = serializers.CharField(source='concessionaire.name')
    comercialdestino = serializers.SerializerMethodField()
    interesado = serializers.SerializerMethodField()
    notas = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = ('identificador', 'fechaalta', 'horaalta', 'nombre', 'apellidos', 'telefono', 'email', 'origen', 'soloventa',
                  'tasacion', 'score', 'estado', 'resultado', 'concesiondestino', 'comercialdestino', 'interesado',
                  'notas')
        # read_only_fields = fields

    def get_interesado(self, obj):
        serializer = PublicVehicleSerializer(obj.vehicles, many=True)
        return {'coche': serializer.data}

    def get_notas(self, obj):
        serializer = PublicNoteSerializer(obj.note.all(), many=True)
        return [{'anotacion': i} for i in serializer.data]

    def get_fechaalta(self, obj):
        return obj.created.strftime("%d/%m/%Y")

    def get_horaalta(self, obj):
        return obj.created.strftime("%T")

    def get_nombre(self, obj):
        return obj.client.name if obj.client else None

    def get_email(self, obj):
        return obj.client.email if obj.client else None

    def get_telefono(self, obj):
        return obj.client.phone if obj.client else None

    def get_origen(self, obj):
        return obj.origin.name if obj.origin else None

    def get_tasacion(self, obj):
        serializer = PublicTaskSerializer(obj.request.task.all(), many=True)
        return [{'coche': i} for i in serializer.data]

    def get_comercialdestino(self, obj):
        return obj.user.first_name if obj.user else None
