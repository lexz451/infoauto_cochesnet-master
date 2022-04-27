# -*- coding: utf-8 -*-
import json


def field_replace(params, keys, replacement):
	"""
	Reemplaza el valores concretos en el diccionario de parámetros de las acciones (Action.http_post_parameters) por el
	valor indicado. Hace una búsqueda recursiva por el diccionario buscando nombres de claves que coincidan con la
	lista de claves pasada como argumento
	:param params:parametros de la accion registrada
	:param keys: str|list  clave o claves a buscar
	:param replacement: cadena que se pondrá en lugar de la original en cada campo que se encuentre
	:return: lista de acciones con valores modificados
	"""
	def replace_item(obj, key, replace_value):
		for k, v in obj.items():
			if isinstance(v, dict):
				obj[k] = replace_item(v, key, replace_value)
		if key in obj:
			obj[key] = replace_value
		return obj
	
	# Ocultamos el campo keys siempre que aparezca
	if type(params) == type(""):
		params =json.loads(params)
	if type(keys) == type(""):
		params = replace_item(params, keys, replacement)
	else:
		for key in keys:
			params = replace_item(params,key,replacement)
	return json.dumps(params)

