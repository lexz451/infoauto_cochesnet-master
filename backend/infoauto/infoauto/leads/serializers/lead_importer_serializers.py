import hashlib
import json
import time
from django.dispatch import Signal
from rest_framework import serializers

from infoauto.common.signals import DisableSignals
from infoauto.countries.models import Province, Locality
from infoauto.leads.models import Concessionaire, LEAD_STATUS, LEAD_RESULT, Lead, Client, Origin, Note
from infoauto.leads.models.clients import CLIENT_TYPE_CHOICES
from infoauto.leads.models.leads import LEAD_RESULT_REASON, SCORE_CHOICES, REQUEST_TYPE_CHOICES
from infoauto.leads.models.tasks import TASK_TYPE, MEDIA, Task, Request
from infoauto.leads.models.vehicles import VEHICLE_TYPE_CHOICES, COMERCIAL_CATEGORY_CHOICES, GasType, Vehicle, ORIGIN, \
    Appraisal
from infoauto.source_channels.models import Channel, Source
from infoauto.users.models import User

import requests

class LeadImporterSerializer(serializers.Serializer):
    concessionaire = serializers.PrimaryKeyRelatedField(queryset=Concessionaire.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    status = serializers.ChoiceField(choices=LEAD_STATUS)
    result = serializers.ChoiceField(choices=LEAD_RESULT, required=False)
    result_reason = serializers.ChoiceField(choices=LEAD_RESULT_REASON, required=False)
    result_comments = serializers.CharField(required=False)
    finish_date = serializers.DateTimeField(required=False)
    score = serializers.ChoiceField(choices=SCORE_CHOICES)
    incoming_call_datetime = serializers.DateTimeField(required=False)
    outgoing_call_datetime = serializers.DateTimeField(required=False)

    request_notes = serializers.CharField(required=False)
    request_type = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES, required=False)

    # Clients fields
    client__name = serializers.CharField(required=False)
    client__surname = serializers.CharField(required=False)
    client__client_type = serializers.ChoiceField(choices=CLIENT_TYPE_CHOICES, required=False)
    client__identification = serializers.CharField(required=False)
    client__business_name = serializers.CharField(required=False)
    client__phone = serializers.CharField(required=False)
    client__desk_phone = serializers.CharField(required=False)
    client__postal_code = serializers.IntegerField(required=False)
    client__email = serializers.EmailField(required=False)
    client__province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), required=False)
    client__location = serializers.PrimaryKeyRelatedField(queryset=Locality.objects.all(), required=False)
    client__address1 = serializers.CharField(required=False)
    client__address2 = serializers.CharField(required=False)

    vehicle__vehicle_type = serializers.ChoiceField(choices=VEHICLE_TYPE_CHOICES, required=False)
    vehicle__comercial_category = serializers.ChoiceField(choices=COMERCIAL_CATEGORY_CHOICES, required=False)
    vehicle__power = serializers.CharField(required=False)
    vehicle__brand_model = serializers.CharField(required=False)
    vehicle__model = serializers.CharField(required=False)
    vehicle__version = serializers.CharField(required=False)
    vehicle__price = serializers.CharField(required=False)
    vehicle__km = serializers.CharField(required=False)
    vehicle__year = serializers.IntegerField(required=False)
    vehicle__gas = serializers.PrimaryKeyRelatedField(queryset=GasType.objects.all(), required=False)
    vehicle__sold = serializers.BooleanField(default=False)
    vehicle__origin = serializers.PrimaryKeyRelatedField(queryset=Origin.objects.all(), required=False)
    vehicle__media = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all(), required=False)
    vehicle__note = serializers.CharField(required=False)

    task__author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    task__type = serializers.ChoiceField(choices=TASK_TYPE, required=False)
    task__description = serializers.CharField(required=False)
    task__media = serializers.ChoiceField(choices=MEDIA, required=False)
    task__planified_realization_date = serializers.DateTimeField(required=False)
    task__realization_date = serializers.DateTimeField(required=False)

    traking__author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    traking__type = serializers.ChoiceField(choices=TASK_TYPE, required=False)
    traking__description = serializers.CharField(required=False)
    traking__media = serializers.ChoiceField(choices=MEDIA, required=False)
    traking__planified_realization_date = serializers.DateTimeField(required=False)
    traking__realization_date = serializers.DateTimeField(required=False)

    appraisal__brand = serializers.CharField(required=False)
    appraisal__model = serializers.CharField(required=False)
    appraisal__version = serializers.CharField(required=False)
    appraisal__km = serializers.CharField(required=False)
    appraisal__status = serializers.CharField(required=False)
    appraisal__features = serializers.CharField(required=False)
    appraisal__circulation_date = serializers.DateTimeField(required=False)
    appraisal__evaluation_vo_price = serializers.IntegerField(required=False)
    appraisal__total_vehicles = serializers.IntegerField(required=False)
    appraisal__total_comercial_vehicles = serializers.IntegerField(required=False)
    appraisal__total_tourism_vehicles = serializers.IntegerField(required=False)
    appraisal__fleet_notes = serializers.CharField(required=False)
    appraisal__license_plate = serializers.CharField(required=False)
    appraisal__buy_date = serializers.DateTimeField(required=False)
    appraisal__registration_date = serializers.DateTimeField(required=False)
    appraisal__last_mechanic_date = serializers.DateTimeField(required=False)
    appraisal__cv = serializers.IntegerField(required=False)
    appraisal__is_finance = serializers.BooleanField(default=False, required=False)
    appraisal__origin = serializers.ChoiceField(choices=ORIGIN, required=False)

    lead_source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all(), required=True)
    lead_note = serializers.CharField(required=False)
    vehicle_ad_link = serializers.CharField(required=False)

    def validate_score(self, value):
        if value:
            return str(value)

    def save(self, **kwargs):
        with DisableSignals():
            request = Request.objects.create()
            client_dict = {
                "name": self.validated_data.get('client__name'),
                "surname": self.validated_data.get('client__surname'),
                "client_type": self.validated_data.get('client__client_type', 'private'),
                "identification": self.validated_data.get('client__identification'),
                "business_name": self.validated_data.get('client__business_name'),
                "phone": self.validated_data.get('client__phone'),
                "desk_phone": self.validated_data.get('client__desk_phone'),
                "postal_code": self.validated_data.get('client__postal_code'),
                "email": self.validated_data.get('client__email'),
                "province": self.validated_data.get('client__province'),
                "location": self.validated_data.get('client__location'),
                "address1": self.validated_data.get('client__address1'),
                "address2": self.validated_data.get('client__address2'),

            }

            client = Client.objects.create(**client_dict)

            lead_dict = {
                "is_imported": True,
                "request": request,
                "concessionaire": self.validated_data.get('concessionaire'),
                "user": self.validated_data.get('user'),
                "status": self.validated_data.get('status'),
                "score": self.validated_data.get('score'),
                "result": self.validated_data.get('result'),
                "result_reason": self.validated_data.get('result_reason'),
                "result_comments": self.validated_data.get('result_comments'),
                "finish_date": self.validated_data.get('finish_date'),
                "source": self.validated_data.get('lead_source'),
                "client": client,
            }

            lead = Lead.objects.create(**lead_dict)

            vehicle_dict = {
                "lead": lead,
                "vehicle_type": self.validated_data.get('vehicle__vehicle_type'),
                "comercial_category": self.validated_data.get('vehicle__comercial_category'),
                "power": self.validated_data.get('vehicle__power'),
                "brand_model": self.validated_data.get('vehicle__brand_model'),
                "model": self.validated_data.get('vehicle__model'),
                "version": self.validated_data.get('vehicle__version'),
                "price": self.validated_data.get('vehicle__price'),
                "km": self.validated_data.get('vehicle__km'),
                "year": self.validated_data.get('vehicle__year'),
                "gas": self.validated_data.get('vehicle__gas'),
                "sold": self.validated_data.get('vehicle__sold'),
                "origin": self.validated_data.get('vehicle__origin'),
                "media": self.validated_data.get('vehicle__media'),
                "note": self.validated_data.get('vehicle__note'),
                "ad_link": self.validated_data.get('vehicle_ad_link')
            }

            vehicle = Vehicle.objects.create(**vehicle_dict)

            if self.validated_data.get('appraisal__brand'):
                appraisal_dict = {
                    "lead": lead,
                    "brand": self.validated_data.get('appraisal__brand'),
                    "model": self.validated_data.get('appraisal__model'),
                    "version": self.validated_data.get('appraisal__version'),
                    "km": self.validated_data.get('appraisal__km'),
                    "status": self.validated_data.get('appraisal__status'),
                    "features": self.validated_data.get('appraisal__features'),
                    "circulation_date": self.validated_data.get('appraisal__circulation_date'),
                    "evaluation_vo_price": self.validated_data.get('appraisal__evaluation_vo_price'),
                    "total_vehicles": self.validated_data.get('appraisal__total_vehicles'),
                    "total_comercial_vehicles": self.validated_data.get('appraisal__total_comercial_vehicles'),
                    "total_tourism_vehicles": self.validated_data.get('appraisal__total_tourism_vehicles'),
                    "fleet_notes": self.validated_data.get('appraisal__fleet_notes'),
                    "license_plate": self.validated_data.get('appraisal__license_plate'),
                    "buy_date": self.validated_data.get('appraisal__buy_date'),
                    "registration_date": self.validated_data.get('appraisal__registration_date'),
                    "last_mechanic_date": self.validated_data.get('appraisal__last_mechanic_date'),
                    "cv": self.validated_data.get('appraisal__cv'),
                    "is_finance": self.validated_data.get('appraisal__is_finance'),
                    "origin": self.validated_data.get('appraisal__origin'),
                }

                appraisal = Appraisal.objects.create(**appraisal_dict)

            if self.validated_data.get('task__author'):
                task_dict = {
                    "lead": lead,
                    "author": self.validated_data.get('task__author'),
                    "type": self.validated_data.get('task__type'),
                    "description": self.validated_data.get('task__description'),
                    "media": self.validated_data.get('task__media'),
                    "realization_date": self.validated_data.get('task__planified_realization_date'),
                    "planified_realization_date": self.validated_data.get('task__realization_date'),
                    "is_traking_task": False
                }

                task = Task.objects.create(**task_dict)
                request.task.add(task)

            if self.validated_data.get('traking__author'):
                traking_dict = {
                    "lead": lead,
                    "author": self.validated_data.get('traking__author'),
                    "type": self.validated_data.get('traking__type'),
                    "description": self.validated_data.get('traking__description'),
                    "media": self.validated_data.get('traking__media'),
                    "realization_date": self.validated_data.get('traking__planified_realization_date'),
                    "planified_realization_date": self.validated_data.get('traking__realization_date'),
                    "is_traking_task": True
                }

                traking = Task.objects.create(**traking_dict)

            if self.validated_data.get('lead_note'):
                note_dict = {
                    "content": self.validated_data.get('lead_note')
                }

                note = Note.objects.create(**note_dict)
                lead.note.add(note)

            self.instance = lead

            c_id = self.instance.concessionaire.id
            c_ids = [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 68, 79, 81, 83, 99, 123]
            if (c_id in c_ids):
                print('-------------------------------------------------')
                print(f'Sending PN request for concessionaire id: {c_id}')
                self.sendPN()
    
    def sendPN(self):
        appKey = 'SAILS'
        consumerKey = '1r9qsfhwmkywvyllxexuw5j54'
        consumerSecret = "CO12345CO"
        url = 'https://drivim.vozipcenter.com/api/nuevo_contacto'
        method = 'POST'

        client_name = str(self.instance.client.name)
        client_phone = str(self.instance.client.phone)

        if (client_phone.startswith('+')):
            client_phone = client_phone.replace('+', '00')
        elif (not client_phone.startswith('00')):
            client_phone = f'00{client_phone}'

        lead_id = self.instance.id
        
        local_time = time.time()
        server_time = int(requests.get('https://drivim.vozipcenter.com/api/time').text)
        diff = server_time - local_time

        data = {
            "modificable": True,
            "grupo": "MARCADOR",
            "nombre": client_name,
            "numero": client_phone,
            "bd": "BBDD",
            "campos": {
                "ID": f"https://sail.artificialintelligencelead.com/leads/{lead_id}/edit"
            }
        }

        print(f'PN payload: {data}')

        payload = json.dumps(data).replace(" ", "")

        timestamp = str(time.time() + diff)

        sha1_payload = f"{consumerSecret}+{consumerKey}+{method}+{url}+{payload}+{timestamp}".encode('utf-8')

        sha1 = hashlib.sha1(sha1_payload).hexdigest()

        signature = "$1$" + sha1

        headers = {
            "Content-Type": "application/json",
            "CC-Application": appKey,
            "CC-Timestamp": timestamp,
            "CC-Signature": signature,
            "CC-Consumer": consumerKey
        }

        req = requests.post(url=url, data=payload, headers=headers)
        print(f'PN response: {req.text}')
        print('-------------------------------------------------')