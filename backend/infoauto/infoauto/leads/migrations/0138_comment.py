# Generated by Django 2.2 on 2022-04-23 23:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0137_auto_20220403_0605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('text', models.TextField()),
                ('origin', models.CharField(choices=[('whatsapp', 'Whatsapp'), ('other', 'Otro')], max_length=100)),
                ('timestamp', models.CharField(max_length=250)),
                ('contact_name', models.CharField(max_length=255)),
                ('event_type', models.CharField(choices=[('templateMessageSent', 'TemplateMessageSent'), ('message', 'Message')], max_length=100)),
                ('wa_id', models.CharField(max_length=255)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.Lead')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
