# Generated by Django 2.2 on 2020-08-27 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0090_vehiclebrand_vehiclemodel_vehicleversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleversion',
            name='size',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
