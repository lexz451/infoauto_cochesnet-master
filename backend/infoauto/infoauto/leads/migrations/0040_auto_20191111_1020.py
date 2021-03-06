# Generated by Django 2.1 on 2019-11-11 09:20

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0039_auto_20191108_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallead',
            name='attended_date',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='is_attended', when={True}),
        ),
        migrations.AddField(
            model_name='historicallead',
            name='is_attended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lead',
            name='attended_date',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='is_attended', when={True}),
        ),
        migrations.AddField(
            model_name='lead',
            name='is_attended',
            field=models.BooleanField(default=False),
        ),
    ]
