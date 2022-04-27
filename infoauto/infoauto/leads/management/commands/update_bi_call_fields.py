import datetime

import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from tqdm import tqdm

from infoauto.leads.models import Task, Lead
from infoauto.netelip.models import CallControlModel
from infoauto.netelip_leads.models import CallControlLeadModel


class Command(BaseCommand):
    help = "Updating call info (CallControlLeadModel) "

    def handle(self, *args, **options):
        queryset = CallControlLeadModel.objects.all()
        description = "Updating call info"
        for call in tqdm(queryset.iterator(), desc=description, total=int(queryset.count())):
            call.save()

        self.stdout.write(self.style.SUCCESS(description))
