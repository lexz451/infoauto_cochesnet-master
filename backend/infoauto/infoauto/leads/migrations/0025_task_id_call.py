# Generated by Django 2.1 on 2019-03-27 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0024_concessionaire_mask_c2c'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='id_call',
            field=models.FloatField(blank=True, help_text='ID único de la llamada', null=True),
        ),
    ]
