# Generated by Django 2.1 on 2019-03-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0023_task_is_click2call'),
    ]

    operations = [
        migrations.AddField(
            model_name='concessionaire',
            name='mask_c2c',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Mascara [src] a mostrar como llamante'),
        ),
    ]
