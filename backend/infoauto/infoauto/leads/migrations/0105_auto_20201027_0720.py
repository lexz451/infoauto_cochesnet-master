# Generated by Django 2.2 on 2020-10-27 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0104_auto_20201027_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallead',
            name='assigned_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='assigned_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
