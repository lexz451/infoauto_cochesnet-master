# -*- coding: utf-8 -*-

"""
Vistas de  log de acciones de usuario
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from . import models
from . import serializers


class LoggedActionView(ListModelMixin, RetrieveModelMixin, GenericViewSet):

	"""
	Servicios para consultar el actionlogging
	"""

	filter_backends = [SearchFilter, DjangoFilterBackend]
	queryset = models.LoggedAction.objects.all()
	serializer_class = serializers.LoggedActionerializerSimple
	filter_fields = {}
	exclude_fields = ['http_get_parameters', 'http_post_parameters', 'response', 'extra']

	def retrieve(self, request, *args, **kwargs):
		self.serializer_class = serializers.LoggedActionerializer
		return super(LoggedActionView, self).retrieve(request, *args, **kwargs)