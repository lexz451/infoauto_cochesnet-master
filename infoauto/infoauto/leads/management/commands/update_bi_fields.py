import datetime

import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from tqdm import tqdm

from infoauto.leads.models import Task, Lead
from infoauto.netelip.models import CallControlModel


class Command(BaseCommand):
    help = "Change task status based on realization date and result"

    def handle(self, *args, **options):

        for lead in tqdm(Lead.objects.all().iterator(),
                         desc="Updating leads",
                         total=int(Lead.objects.all().count())):

            lead.update_status_metrics()
            lead.update_call_metrics()

        msg = 'Updated lead info'
        self.stdout.write(self.style.SUCCESS(msg))
