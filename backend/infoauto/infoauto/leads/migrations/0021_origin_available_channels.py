# Generated by Django 2.1 on 2019-01-28 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source_channels', '0003_auto_20190128_1116'),
        ('leads', '0020_lead_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='origin',
            name='available_channels',
            field=models.ManyToManyField(blank=True, to='source_channels.Channel'),
        ),
    ]
