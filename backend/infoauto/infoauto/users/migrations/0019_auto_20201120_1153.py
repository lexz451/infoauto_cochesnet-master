# Generated by Django 2.2 on 2020-11-20 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20200720_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='ubunet_company',
            field=models.CharField(blank=True, default=None, help_text='Company en Ubunet', max_length=17, null=True),
        ),
        migrations.AddField(
            model_name='historicaluser',
            name='ubunet_extension',
            field=models.CharField(blank=True, default=None, help_text='Extension en Ubunet', max_length=17, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ubunet_company',
            field=models.CharField(blank=True, default=None, help_text='Company en Ubunet', max_length=17, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ubunet_extension',
            field=models.CharField(blank=True, default=None, help_text='Extension en Ubunet', max_length=17, null=True),
        ),
    ]
