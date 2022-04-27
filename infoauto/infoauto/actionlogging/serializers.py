# -*- coding: utf-8 -*-

"""
Serializador para el log de acciones
"""

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from . import models

class LoggedActionerializerSimple(ModelSerializer):
	"""
	Serializador simple para el log de acciones
	"""

	# usuario que ejecuta la acción
	executor_user = serializers.SerializerMethodField()

	# usuario que suplanta
	impersonate_user = serializers.SerializerMethodField()

	def get_executor_user(self, obj):
		user = obj.executor_user
		return user.username if user else ""

	def get_impersonate_user(self, obj):
		user = obj.impersonate_user
		return user.username if user else ""


	class Meta(object):
		model = models.LoggedAction
		fields = ('id', 'creation_datetime', 'action', 'url', 'executor_user', 'impersonate_user')


class LoggedActionerializer(LoggedActionerializerSimple):

	"""
	Serializador para el log de acciones
	"""

	class Meta(object):
		model = models.LoggedAction
		fields = '__all__'

