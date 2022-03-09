# -*- coding: utf-8 -*-

import json
from django.conf import settings
from .models import LoggedAction
from django.apps import apps


from django.utils.deprecation import MiddlewareMixin


def exists_url(url, action):
    import re

    """
    Function that searches within an array of objects action,url and checks for matches
    :param array:
    :param url:
    :return:
    """
    array = settings.ACTIONLOGGING_ENABLE_URL

    try:
        for obj in array:
            if bool(re.findall(obj["url"], str(url))) and action in obj["actions"]:
                return True
        return False
    except Exception:
        return False


class ActionLoggingMiddleware(MiddlewareMixin):
    
    last_view = None
    
    def process_request(self, request):
        request.request_data = request.body
        request.log = []

    def process_view(self, request, view, args, kwargs):
        # Instanciamos la última vista
        self.last_view = view

    def process_response(self, request, response):

        this_url = request.build_absolute_uri()

        # Check if the current url if the target of this middleware,
        # matching with ACTIONLOGGING_ENABLE_URL in setting.
        if not exists_url(this_url, request.method):
            return response

        description = ""
        for log in request.log:
            description += log + " "

        # Vista a la que se accede
        try:
            cls = self.last_view.cls

            # Nombre del subsistema
            subsystem = cls.__name__

            # Revisamos que la vista tenga el atributo save_log a True para guardar el log de acciones
            save_log = cls.save_log if hasattr(cls, "save_log") else settings.ACTIONLOGGING_SAVE_LOG

        except:
            subsystem = request.path
            save_log = None
            cls = None

        try:
            # Nombre del paquete al que pertenece la vista
            system = request.path.split("/api/")[1].split("/")[0]
        except:
            system = "INFOAUTO"

        if hasattr(self.last_view, "save_log") or save_log or cls is None:
            response_obj = response
            LoggedAction.create_from_request(
                request=request,
                system=system,
                subsystem=subsystem,
                action=request.method,
                description=description,
                response=response_obj
            )

        return response
