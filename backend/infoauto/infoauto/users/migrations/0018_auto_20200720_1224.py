# Generated by Django 2.2 on 2020-07-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20200702_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='unavailable_reason',
            field=models.CharField(blank=True, choices=[('asisting_clients', 'Atendiendo clientes'), ('breakfast', 'Desayunando'), ('bathroom', 'En el aseo'), ('excused', 'Ausencia justificada')], help_text='Motivo trabajador no se encuentra disponible', max_length=512),
        ),
        migrations.AlterField(
            model_name='user',
            name='unavailable_reason',
            field=models.CharField(blank=True, choices=[('asisting_clients', 'Atendiendo clientes'), ('breakfast', 'Desayunando'), ('bathroom', 'En el aseo'), ('excused', 'Ausencia justificada')], help_text='Motivo trabajador no se encuentra disponible', max_length=512),
        ),
    ]
