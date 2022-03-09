# -*- coding: utf-8 -*-

###########################################
# Models methods
from django.contrib.auth import get_user_model
from django.db import models, DatabaseError, connection
from django.conf import settings
from django.utils import timezone

from .utils import field_replace

import json

########################################################################
########################################################################

User = get_user_model()

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


# Método HTTP
HTT_METHODS = (
	(u"GET", u"GET"),
	(u"HEAD", u"HEAD"),
	(u"POST", u"POST"),
	(u"PUT", u"PUT"),
	(u"DELETE", u"DELETE")
)


# Permite almacenar las acciones
class LoggedAction(models.Model):

	# Metainformación de la clase LoggedAction
	class Meta:
		ordering = ["-creation_datetime", "system"]
		verbose_name = "acción registrada"
		verbose_name_plural = "acciones registradas"

		index_together = (
			("creation_datetime", "system", "subsystem", "action"),
			("ip", "creation_datetime", "system", "subsystem", "action"),
			("executor_user", "creation_datetime", "system", "subsystem", "action"),
			("executor_user", "is_staff", "creation_datetime", "system", "subsystem", "action")
		)
	
	# Fecha y hora que indica cuándo se ha producido la acción
	creation_datetime = models.DateTimeField(
		verbose_name=u"Fecha y hora de la operación", help_text=u"Fecha y hora en la que se ha realizado la acción."
	)
	
	# Sistema que ha actuado
	system = models.CharField(
		null=True, default=None, max_length=64, verbose_name=u"Sistema",
		help_text=u"Sistema del que depende la operación."
	)
	
	# Subsistema que ha actuado
	subsystem = models.CharField(
		null=True, default=None, max_length=64, verbose_name=u"Subsistema",
		help_text=u"Subsistema del que depende la operación."
	)
	
	# Descripción corta de la acción
	action = models.CharField(
		null=True, default=None, max_length=256, verbose_name=u"Acción", help_text=u"Acción ejecutada."
	)
	
	# Descripción larga de la acción
	description = models.CharField(
		verbose_name=u"Descripción", help_text=u"Descripción de la acción ejecutada.", max_length=1024
	)
	
	# URL a la que se ha hecho la petición
	url = models.CharField(
		max_length=1024, verbose_name=u"Dirección URL",
		help_text=u"Dirección URL llamada para la ejecución de la acción."
	)
	
	# Parámetros GET de la petición
	http_get_parameters = models.TextField(
		null=True, default=None, verbose_name=u"Parámetros GET",
		help_text=u"Parámetros GET recibidos por el servidor."
	)
	
	# Parámetros POST de la petición
	http_post_parameters = models.TextField(
		null=True, default=None, verbose_name=u"Parámetros POST",
		help_text=u"Parámetros POST recibidos por el servidor."
	)
	
	# Método HTTP de la petición
	http_method = models.CharField(
		max_length=32, default=u"get", choices=HTT_METHODS, verbose_name=u"Método HTTP", help_text=u"Método HTTP."
	)
	
	# Agente de usuario del cliente
	http_user_agent = models.CharField(
		verbose_name=u"Agente de usuario del cliente", max_length=1024,
		help_text=u"Agente de usuario que envía el navegador al servidor."
	)
	
	# Dirección IP del cliente
	ip = models.GenericIPAddressField(
		verbose_name=u"Dirección IP", help_text=u"Dirección IP del cliente que ejecuta esta acción."
	)
	
	# Usuario ejecutor
	executor_user = models.ForeignKey(
		User, null=True, default=None, related_name='logged_actions',
		verbose_name="Usuario que ha realizado la operación",
		help_text="Usuario que ha realizado la operación.", on_delete=models.SET_NULL
	)

	# Guarda el usuario que ha sido impersonado.
	impersonate_user = models.ForeignKey(
		User, null=True, default=None, related_name='impersonated_logged_actions', verbose_name="Usuario impersonado",
		help_text="Usuario impersonado", on_delete=models.SET_NULL
	)

	# Datos extra
	extra = models.TextField(
		null=True, default=None, verbose_name=u"Datos extra", help_text=u"Datos extra de utilidad."
	)
	
	# Indica si el usuario que realiza la acción es "staff" del sitio web
	is_staff = models.BooleanField(
		default=False, verbose_name="Acción realizada por personal de la aplicación",
		help_text="Indica si esta acción ha sido realizada por personal interno"
	)
	
	# Response de la petición
	response = models.TextField(
		null=True, default=None, verbose_name=u"Respuesta de la acción",
		help_text=u"Respuesta que provoca la acción"
	)
	
	status_code = models.CharField(
		max_length=32, verbose_name=u"Código de la respuesta",
		help_text=u"Código de la respuesta",null=True, default=None,
	)

	####################################################################
	# Crea un objeto LoggedAction a partir de una petición request y
	# otros parámetros
	####################################################################

	@staticmethod
	def create_from_request(
			request,
			description,
			system=None,
			subsystem=None,
			action=None,
			extra=None,
			executor_user=None,
			hide_params=None,
			hide_text=None,
			response=None
	):
		"""
		Crea un registro de acción a partir de una petición request y otros datos
		:param request: request de la llamada
		:param description: descripción de la llamada, por ejemplo, Creación de un nuevo convenio o Descarga del pdf del convenio 15
		:param system: Sistema o paquete que invocado
		:param subsystem: Subsistema invocado
		:param action: accion POS GET,UPDATE, etc
		:param extra: {} argumentos extra a almacenar
		:param executor_user: request.user Usuario que invoca la acción
		:param hide_params: [], Lista de parametros a ocultar su contenido, por ejemplo, ["password","password1","password2"]
		:return:
		"""

		# Para acciones de usuarios anónimos (como por ejemplo la venta)
		executor_user = executor_user
		if not executor_user and request.user and request.user.is_authenticated:
			executor_user = request.user
		
		# Si no le pasas texto para reemplazar coge el del settings
		if not hide_text:
			ACTIONLOGGING_TEXT_HIDE_REQUEST = settings.ACTIONLOGGING_TEXT_HIDE_REQUEST
		
		# Parámetros post
		if len(request.POST.dict()) != 0:
			postdata = json.dumps(request.POST.dict())
		else:
			postdata = request.body.decode('utf-8')

		if postdata:
			# Oculta los parámetros indicados en el settings
			postdata = field_replace(postdata, settings.ACTIONLOGGING_FIELDS_HIDE_REQUEST, hide_text)
		
			# Oculta los hide_params
			if hide_params is not None:
				postdata = field_replace(postdata, hide_params, ACTIONLOGGING_TEXT_HIDE_REQUEST)
			
			# Oculta los hide params de los extra
			if extra is not None:
				extra = field_replace(extra, hide_params, ACTIONLOGGING_TEXT_HIDE_REQUEST)

		# Por defecto asumimos que no existe impersonate.
		impersonate_user = None

		try:
			response_data = json.loads(response.content.decode('utf-8'))
			response_data = json.dumps(response_data)
		except:
			response_data = response
			
		# Parámetros para construir un registro de acción
		parameters = {
			"system": system,
			"subsystem": subsystem,
			"action": action,
			"description": description,
			"url": request.build_absolute_uri(),
			"http_get_parameters": json.dumps(request.GET.dict()),
			"http_post_parameters": postdata,
			"http_method": request.method,
			"http_user_agent": request.META.get("HTTP_USER_AGENT") or "",
			"ip": get_client_ip(request),
			"executor_user": executor_user,
			"impersonate_user": impersonate_user,
			"extra": extra,
			"is_staff": request.user.is_staff,
			"response": response_data,
			"status_code": response.status_code if response is not None else None
		}

		action = LoggedAction(**parameters)

		try:
			action.save()
		except DatabaseError:

			# En caso de que se produzca un error tratando de guardar el action loggin,
			# tratamos de guardar la operación con menos campos.
			parameters = {
				"system": system,
				"subsystem": subsystem,
				"action": action,
				"description": description,
				"url": request.build_absolute_uri(),
				"http_method": request.method,
				"http_user_agent": request.META.get("HTTP_USER_AGENT") or "",
				"ip": get_client_ip(request),
				"executor_user": executor_user,
				"impersonate_user": impersonate_user,
				"is_staff": request.user.is_staff,
				"status_code": response.status_code if response is not None else None
			}

			action = LoggedAction(**parameters)
			action.save()
		return action

	@staticmethod
	def create_without_request(description, system=None, subsystem=None, action=None, extra=None, hide_params=None):
		"""
		Crea un objeto LoggedAction de una serie parámetros
		:param description:
		:param system:
		:param subsystem:
		:param action:
		:param extra:
		:param hide_params:
		:return:
		"""

		parameters = {
			"system": system,
			"subsystem": subsystem,
			"action": action,
			"description": description,
			"extra": extra,
			"ip": "127.0.0.1"
		}
		action = LoggedAction(**parameters)
		action.save()
		return action

	def save(self, *args, **kwargs):

		"""
		Save object in database, updating the datetimes accordingly.
		"""

		if not self.pk:
			self.creation_datetime = timezone.now()
		else:
			raise AssertionError(u"No puedes editar acciones registradas")

		super(LoggedAction, self).save(*args, **kwargs)
