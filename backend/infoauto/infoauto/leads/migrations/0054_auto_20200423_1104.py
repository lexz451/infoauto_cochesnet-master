# Generated by Django 2.1 on 2020-04-23 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0053_auto_20200421_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallead',
            name='requests_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='requests_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
