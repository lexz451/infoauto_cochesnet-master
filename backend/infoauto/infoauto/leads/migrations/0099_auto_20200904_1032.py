# Generated by Django 2.2 on 2020-09-04 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0098_import_vehicles_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicallead',
            name='hubspot_status',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='hubspot_status',
        ),
    ]
