import os

from django.db import migrations
from django.db.migrations import RunSQL


def manage_view(sql_file_name):
    app_path = os.path.join(os.path.dirname(__file__), sql_file_name)
    file = open(app_path, 'r')
    sql_txt = file.read()
    file.close()
    return sql_txt


class Migration(migrations.Migration):

    dependencies = [
        ('sql_views', '0006_create_calendar_view'),
    ]

    operations = [
        RunSQL(manage_view('create_calendar_view.sql'))
    ]
