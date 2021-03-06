# Generated by Django 2.2 on 2020-07-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0074_auto_20200703_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='buy_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='cv',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='is_finance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='last_mechanic_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='registration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
