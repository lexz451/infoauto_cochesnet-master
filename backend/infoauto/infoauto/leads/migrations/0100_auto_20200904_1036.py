# Generated by Django 2.2 on 2020-09-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0099_auto_20200904_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallead',
            name='hubspot_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lead',
            name='hubspot_status',
            field=models.BooleanField(default=False),
        ),
    ]
