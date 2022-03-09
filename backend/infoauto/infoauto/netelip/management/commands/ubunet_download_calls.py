import datetime
import errno
import json
import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Q

from infoauto.common.util_email import send_email
from infoauto.leads.models import Lead
from infoauto.netelip.client import Click2CallUbunetClient
from infoauto.netelip.models import CallControlModel
from infoauto.netelip.utils import get_recorded_call
from infoauto.netelip_leads.models import CallControlLeadModel


class Command(BaseCommand):
    help = "Descarga llamadas desde Ubunet"

    def handle(self, *args, **options):

        try:
            os.makedirs(settings.MEDIA_ROOT + '/audios/')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        client = Click2CallUbunetClient()

        for call_obj in CallControlModel.objects.filter(api='UBUNET', ubunet_audio_downloaded=False):
            audio_response = client.download_audio(int(call_obj.id_call))
            if audio_response.status_code == 200:
                with open(settings.MEDIA_ROOT + '/audios/' + str(call_obj.id_call) + '.mp3', 'wb') as f:
                    audio_file = File(f)
                    audio_file.write(audio_response.content)
                print(f"Downloaded {str(call_obj.id_call)}.mp3")
                call_obj.ubunet_audio_downloaded = True
                call_obj.save()

        for call_obj in CallControlModel.objects.filter(description__startswith='/APIVoice/Record/', ubunet_audio_downloaded=False):
            try:
                local_path = get_recorded_call(call_obj)
                if local_path:
                    with open(local_path, 'rb') as local_file:
                        with open(settings.MEDIA_ROOT + '/audios/' + str(call_obj.id_call) + '.mp3', 'wb') as f:
                            audio_file = File(f)
                            audio_file.write(local_file.read())
                    print(f"Downloaded {str(call_obj.id_call)}.mp3")
                    call_obj.ubunet_audio_downloaded = True
                    call_obj.save()
            except:
                call_obj.ubunet_audio_downloaded = True
                call_obj.save()

