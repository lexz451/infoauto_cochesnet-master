# Generated by Django 2.1 on 2019-01-25 14:00

from django.db import migrations


def default_channels(apps, schema_editor):
    Channel = apps.get_model('source_channels', 'Channel')
    default_data = [{'slug': 'phone', 'name': 'Teléfono'}, {'slug': 'email', 'name': 'Email'},
                    {'slug': 'chat', 'name': 'Chat'}, {'slug': 'exposition', 'name': 'Exposición'},
                    {'slug': 'web_home', 'name': 'Web Home'}]
    [Channel.objects.create(**i) for i in default_data]


class Migration(migrations.Migration):

    dependencies = [
        ('source_channels', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_channels, reverse_code=migrations.RunPython.noop),
    ]
