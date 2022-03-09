# -*- coding: utf-8 -*-

from django.conf import settings
from django.core import mail
from django.template import loader, Context, RequestContext


########################################################################
########################################################################


def render_content(template, context=None, request=None):
    """Renderiza el contenido para un email a partir de la plantilla y el contexto.
    Deben existir las versiones ".html" y ".txt" de la plantilla.

    Adicionalmente, si se recibe el request, se utilizará para el renderizado.

    """
    context = context or {}

    if request:
        render_params = {"context": context, "request": request}
        #~ context["request"] = request
    else:
        #~ context = context
        render_params = {"context": context}

    return {
        "text_content": loader.get_template(u'{0}.txt'.format(template)).render(**render_params),
        "html_content": loader.get_template(u'{0}.html'.format(template)).render(**render_params)
    }


def get_connection(smtp_config_name):
    """Devuelve la conexión SMTP a utilizar, en caso de que sea necesario.

    Será necesario instanciar una conexión SMTP si se recibe el nombre de una
    configuración SMTP a utilizar de las definidas en settings (y ésta existe).

    """

    try:
        smtp_config = settings.SMTP_CONFIG
    except:
        smtp_config = None

    if smtp_config and smtp_config_name and smtp_config_name in smtp_config:
        use_tls = False
        use_ssl = False

        if "use_tls" in smtp_config[smtp_config_name]:
            use_tls = smtp_config[smtp_config_name]["use_tls"]

        if "use_ssl" in smtp_config[smtp_config_name]:
            use_ssl = smtp_config[smtp_config_name]["use_ssl"]

        connection = mail.get_connection(
            host=smtp_config[smtp_config_name]["host"],
            port=smtp_config[smtp_config_name]["port"],
            username=smtp_config[smtp_config_name]["username"],
            password=smtp_config[smtp_config_name]["password"],
            use_tls=use_tls, use_ssl=use_ssl, fail_silently=False)
    else:
        connection = mail.get_connection()

    return connection


def get_from_email(from_email_received, smtp_config_name):
    """Resuelve el "form_email" a utilizar en función del recibido.

    Si se recibe uno, se utiliza ese.
    Si no se recibe se utiliza el definido por defecto en settings o el establecido
    para la configuración SMTP correspondiente, en caso de que se indique alguna.

    """

    if from_email_received:
        return from_email_received

    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        smtp_config = settings.SMTP_CONFIG
    except:
        smtp_config = None

    if smtp_config and smtp_config_name and smtp_config_name in smtp_config:
        if "from_email" in smtp_config[smtp_config_name]:
            from_email = smtp_config[smtp_config_name]["from_email"]

    return from_email


def get_email(to_email, subject, template, from_email=None, context=None, request=None, smtp_config_name=None, cc=None, bcc=None):
    """Instancia un objeto de EmailMultiAlternative a partir de los datos recibidos."""
    context = context or {}
    if not isinstance(to_email, list) and not isinstance(to_email, dict):
        to_email = [to_email]

    from_email_resolved = get_from_email(from_email, smtp_config_name)

    content = render_content(template, context, request)
    text_content = content["text_content"]
    html_content = content["html_content"]

    connection = get_connection(smtp_config_name)
    msg = mail.EmailMultiAlternatives(subject, text_content, from_email_resolved, to_email, connection=connection, cc=cc, bcc=bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.content_subtype = "html"

    return msg


def get_email_from_content(to_email, subject, html_content, text_content, from_email=None, smtp_config_name=None, cc=None, bcc=None):
    """Devuelve una instancia de EmailMultiAlternatives instanciada siendo recibido
    el texto del correo ya renderizado en la llamada a la función.

    """

    if not isinstance(to_email, list) and not isinstance(to_email, dict):
        to_email = [to_email]

    connection = get_connection(smtp_config_name)
    from_email_resolved = get_from_email(from_email, smtp_config_name)

    msg = mail.EmailMultiAlternatives(subject, text_content, from_email_resolved, to_email, connection=connection, cc=cc, bcc=bcc)
    msg.attach_alternative(html_content, "text/html")

    return msg


def send_email(to_email, subject, template, from_email=None, context=None,
               request=None, smtp_config_name=None, cc=None, bcc=None):
    """Envío de un email."""
    context = context or {}

    msg = get_email(to_email, subject, template, from_email, context, request, smtp_config_name, cc, bcc)
    msg.send()


def send_email_from_content(to_email, subject, html_content, text_content, from_email=None, smtp_config_name=None, cc=None, bcc=None):

    msg = get_email_from_content(to_email, subject, html_content, text_content, from_email, smtp_config_name, cc, bcc)
    msg.send()


def send_emails(emails_config, smtp_config_name=None):
    """Envío de varios emails haciendo uso de una única conexión."""

    if emails_config:
        connection = get_connection(smtp_config_name)
        emails = [get_email(**email_config) for email_config in emails_config]
        connection.send_messages(emails)
