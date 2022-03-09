# -*- coding: utf-8 -*-
from django.utils import six
from rest_framework import serializers

from . import models


################################################################################


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """Clase base para un ModelSerializer que nos permite indicar, al instanciarlo,
    los campos que se quieren obtener.
    http://www.django-rest-framework.org/api-guide/serializers#dynamically-modifying-fields
    
    Cuando una clase herede de ésta se podrán indicar los parámetros de las tres
    formas siguientes (ordenadas en orden ascendente de prioridad, de forma
    que si se utilizan varias sólo se tendrá en cuenta la de nivel superior):
    1- Mediante un atributo "fields" dentro de una clase "Meta", de la forma usual
    2- Mediante un parámetro "fields" pasado al instanciar el serializador
    3- Mediante un atributo "default_fields" añadido en al definición de la clase
       serializadora.
    
    Al heredar de esta clase, lo normal será establecer el 
    atributo "default_fields" (3) para establecer los campos que se añadirán por
    defecto al serializar y utilizar la forma 2 cuando se desee utilizar otro
    conjunto de campos en la serialización. Por lo tanto, no tiene sentido heredar
    de esta clase y utilizar la forma 1 para indicar los campos a utilizar en el
    proceso de serialización.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        
        if not fields and hasattr(self, "default_fields"):
            fields = self.default_fields
    
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        # Eliminar los campos que están excluidos (están en exclude)
        elif exclude:
            not_allowed = set(exclude)
            existing = set(self.fields.keys())
            
            for field_name in existing:
                if field_name in not_allowed:
                    self.fields.pop(field_name)
    
    def perform_validation(self, attrs):
        """Se sobreescribe para hacer "trim" a los campos de texto"""
        
        for field_name, value in attrs.items():
            if isinstance(value, six.string_types):
                attrs[field_name] = value.strip()
        
        return super(DynamicFieldsModelSerializer, self).perform_validation(attrs)


class CountrySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = models.Country
        fields = ("id", "iso", "name", "status")


class ProvinceSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = models.Province
        fields = ("id", "country", "name", "status")


class LocalitySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = models.Locality
        fields = ("id", "province", "name", "status")


##########################################################################
class CountryFullSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = models.Country
        fields = ("id","name",)


class ProvinceFullSerializer(DynamicFieldsModelSerializer):

    country = CountryFullSerializer()

    class Meta:
        model = models.Province
        fields = ("id","country", "name")


class LocalityFullSerializer(DynamicFieldsModelSerializer):

    province = ProvinceFullSerializer()


    class Meta:
        model = models.Locality
        fields = ("id", "province", "name")
