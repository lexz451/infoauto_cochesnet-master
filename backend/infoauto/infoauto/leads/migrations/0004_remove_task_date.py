# Generated by Django 2.1 on 2018-10-02 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20181001_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='date',
        ),
    ]
