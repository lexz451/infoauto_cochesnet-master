# Generated by Django 2.1 on 2019-01-28 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('source_channels', '0001_initial'),
        ('leads', '0019_lead_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='source_channels.Source'),
        ),
    ]
