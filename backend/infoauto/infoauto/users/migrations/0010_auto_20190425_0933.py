# Generated by Django 2.1 on 2019-04-25 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190325_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsessionwithhistoric',
            name='history_change_reason',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='history_change_reason',
            field=models.TextField(null=True),
        ),
    ]
