# Generated by Django 2.1 on 2019-01-15 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0016_auto_20190109_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
