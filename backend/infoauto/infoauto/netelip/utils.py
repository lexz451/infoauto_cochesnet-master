import datetime
import errno
import json
import os

from django.conf import settings
from django.core.files import File
from django.db import IntegrityError
from django.utils import timezone

from infoauto.common.util_email import send_email
from infoauto.leads.models import Lead
from infoauto.leads.models.lead_management import LeadManagement, EVENT_INCOMING_CALL_KEY
from infoauto.netelip.client import Click2CallUbunetClient
from infoauto.netelip.models import CallControlModel
from infoauto.netelip.webdav3 import WebDAVClient
from infoauto.netelip_leads.models import CallControlLeadModel
from infoauto.users.models import User


def get_record_description(call_instance):
    description = None
    if call_instance.description.startswith("/APIVoice/Record/"):
        description = call_instance.description
    else:
        descriptions = [i for i in call_instance.history.all().values_list('description', flat=True)
                        if i and i.startswith("/APIVoice/Record/")]
        if descriptions:
            description = descriptions[0]
    return description


def get_recorded_call(call_instance):
    """
    Get local path to audio file if exists
    :param call_instance: CallControlModel instance
    :return: (local_path|None)
    """
    description = get_record_description(call_instance)
    if description:
        client = WebDAVClient(settings.BASE_NETELIP_WEVDAV)
        local_path = '/tmp/%s' % get_record_file_name(call_instance)
        client.download(remote_path=description, local_path=local_path)
        return local_path
    return None


def get_record_file_name(call_instance):
    splitted_file_path = None
    description = get_record_description(call_instance)
    if description:
        splitted_file_path = description.split('/')
        splitted_file_path.reverse()
    return splitted_file_path[0]


def check_calls():

    queryset = CallControlModel.objects.filter(is_checked=False, call_origin="client")

    if queryset:
        call_control_lead_array = []
        created = False

        for call in queryset.iterator():
            user = None
            message = "Llamada recibida"
            if call.api == 'UBUNET':
                message += ' ' + str(call.durationcallanswered)
            if call.api == 'UBUNET' and call.ubunet_agent is not None:
                users = User.objects.filter(ubunet_agent=call.ubunet_agent)
                if not users.exists():
                    users = User.objects.filter(phone=call.ubunet_agent)
                if users.exists():
                    user = users.first()

            leads = Lead.objects.filter(
                client__phone=call.src,
                source__data__icontains=call.dst
            ).exclude(status='end')

            if not leads.exists() and user is not None:
                leads = Lead.objects.filter(
                    client__phone=call.src,
                    user=user
                ).exclude(status='end')

            if leads.exists():
                lead = leads.first()

                if not user:
                    user = lead.user

                try:
                    call_control_lead = CallControlLeadModel.objects.create(
                        lead=lead,
                        call_control=call,
                        user=user
                    )

                    LeadManagement.objects.create(
                        lead=call_control_lead.lead,
                        user=user,
                        event=EVENT_INCOMING_CALL_KEY,
                        status=call_control_lead.lead.status,
                        message=message
                    )

                except IntegrityError as e:
                    print(e)

                if created:
                    call_control_lead_array.append(call_control_lead)
                    notify(lead)

            call.is_checked = True
            call.save()

        msg = "Checked calls: {}".format(len(call_control_lead_array))

    else:
        msg = 'No call to check'

    queryset = CallControlModel.objects.filter(is_checked=False, call_origin="user", ubunet_extension__isnull=False)

    for call in queryset.iterator():

        leads = Lead.objects.filter(
            client__phone=call.dst,
            user__ubunet_company=call.ubunet_company,
            user__ubunet_extension__in=('M' + call.ubunet_extension, 'F' + call.ubunet_extension)
        ).order_by('-created')

        if not leads.exists():
            leads = Lead.objects.filter(
                client__phone=call.dst,
                concessionaire__userconcession__user__ubunet_company=call.ubunet_company,
                concessionaire__userconcession__user__ubunet_extension__in=('M' + call.ubunet_extension, 'F' + call.ubunet_extension)
            ).order_by('-created')

        if leads.exists():
            lead = leads.first()

            try:
                CallControlLeadModel.objects.get_or_create(
                    lead=lead, call_control=call, defaults={'user': lead.user}
                )
            except IntegrityError as e:
                print(e)

        call.is_checked = True
        call.save()


def ubunet_calls():
    try:
        os.makedirs(settings.MEDIA_ROOT + '/audios/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    last_time = timezone.now() - datetime.timedelta(minutes=10)
    for call_obj in CallControlModel.objects.filter(description__startswith='/APIVoice/Record/',
                                                    ubunet_audio_downloaded=False, created__gt=last_time):
        local_path = get_recorded_call(call_obj)
        if local_path:
            with open(local_path, 'rb') as local_file:
                with open(settings.MEDIA_ROOT + '/audios/' + str(call_obj.id_call) + '.mp3', 'wb') as f:
                    audio_file = File(f)
                    audio_file.write(local_file.read())
            print(f"Downloaded {str(call_obj.id_call)}.mp3")
            call_obj.ubunet_audio_downloaded = True
            call_obj.save()

    CallControlLeadModel.objects.filter(call_control__isnull=True).delete()

    client = Click2CallUbunetClient()
    response = client.get_calls()
    results = json.loads(response.content)

    for call in results['data']:
        if not CallControlModel.objects.filter(id_call=call['id']).exists():
            data = {
                'id_call': call['id'],
                'api': 'UBUNET',
                'src': call['caller'],
                'dst': call['inddi'],
                'startcall': datetime.datetime.strptime(call['time'], '%Y-%m-%d %H:%M:%S'),
                'durationcall': datetime.timedelta(seconds=int(call['duration'])),
                'durationcallanswered': datetime.timedelta(seconds=int(call['duration'])),
                'description': 'Llamada usando UBUNET',
                'statuscall': 'NOANSWER' if call['result'] in ['Abandon', 'Timeout'] else call['result'],
                'call_origin': 'client',
                'is_checked': False,
                'ubunet_agent': call['agent'],
                'ubunet_holdtime': datetime.timedelta(seconds=int(call['holdtime'])),
            }
            call_obj = CallControlModel.objects.create(**data)
            call_obj.created = datetime.datetime.strptime(call['time'], '%Y-%m-%d %H:%M:%S')
            call_obj.save()

            audio_response = client.download_audio(call['id'])
            if audio_response.status_code == 200:
                with open(settings.MEDIA_ROOT + '/audios/' + str(call_obj.id_call) + '.mp3', 'wb') as f:
                    audio_file = File(f)
                    audio_file.write(audio_response.content)
                call_obj.ubunet_audio_downloaded = True
                call_obj.save()

    response = client.get_outgoing_calls()
    results = json.loads(response.content)

    for call in results['data']:
        call['id'] = int(call['id']) * -1
        if call["type"] == 'outgoing' and not CallControlModel.objects.filter(id_call=call['id']).exists():
            data = {
                'id_call': call['id'],
                'api': 'UBUNET',
                'src': call['src'],
                'dst': call['dst'],
                'startcall': datetime.datetime.strptime(call['calldate'], '%Y-%m-%d %H:%M:%S'),
                'durationcall': datetime.timedelta(seconds=int(call['billsec'])),
                'durationcallanswered': datetime.timedelta(seconds=int(call['billsec'])),
                'description': 'Click2Call usando UBUNET',
                'statuscall': 'ANSWER' if int(call['billsec']) > 0 else 'CANCEL',
                'call_origin': 'user',
                'is_checked': True,
                'ubunet_company': call['src_company'],
                'ubunet_extension': call['src_extension']
            }
            call_obj = CallControlModel.objects.create(**data)
            call_obj.created = datetime.datetime.strptime(call['calldate'], '%Y-%m-%d %H:%M:%S')
            call_obj.save()

            leads = Lead.objects.filter(
                client__phone=call_obj.dst,
                user__ubunet_company=call['src_company'],
                user__ubunet_extension__in=('M' + call['src_extension'], 'F' + call['src_extension'])
            ).exclude(status='end')

            if leads.exists():
                lead = leads.first()

                try:
                    CallControlLeadModel.objects.get_or_create(
                        lead=lead, call_control=call_obj, defaults={'user': lead.user}
                    )
                except IntegrityError as e:
                    print(e)

            audio_response = client.download_audio_c2c(call['id'])
            if audio_response and audio_response.status_code == 200:
                with open(settings.MEDIA_ROOT + '/audios/' + str(call_obj.id_call) + '.mp3', 'wb') as f:
                    audio_file = File(f)
                    audio_file.write(audio_response.content)
                call_obj.ubunet_audio_downloaded = True
                call_obj.save()


def notify(lead):
    try:
        send_email(to_email=[lead.user.email],
                   subject='Llamada de tu cliente {0}'.format(lead.client.name),
                   template='email/assign_lead',
                   context={"lead": lead},
                   smtp_config_name="default")
    except Exception as e:
        print(e)
