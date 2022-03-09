import datetime

import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from infoauto.leads.models import Task


class Command(BaseCommand):
    help = "Change task status based on realization date and result"

    def handle(self, *args, **options):
        queryset = Task.objects.filter(realization_date__lt=datetime.datetime.now(
                                           tz=pytz.timezone(settings.TIME_ZONE)),
                                       realization_date_check=False)
        if queryset:
            for i in queryset:
                # i.status = 'timeout'
                i.save()
            msg = "Updated tasks: %s" % (list(queryset.values_list('id', flat=True)))
        else:
            msg = 'No Tasks updated'
        self.stdout.write(self.style.SUCCESS(msg))
