import datetime

import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from infoauto.leads.models import Task
import os
from django.db import connection
from django.db import connection, transaction


def manage_view(sql_file_name):

    app_path = os.path.join(os.path.dirname(__file__), '..', '..', 'migrations', sql_file_name)
    file = open(app_path, 'r')
    sql_txt = file.read()

    with connection.schema_editor() as schema_editor:
        schema_editor.execute(sql_txt, params=None)

    file.close()
    return app_path


class Command(BaseCommand):
    help = "Change task status based on realization date and result"

    def handle(self, *args, **options):
        manage_view('update_views.sql')
        msg = 'Mysql views updated successfully, using update_views.sql script =)'
        self.stdout.write(self.style.SUCCESS(msg))
