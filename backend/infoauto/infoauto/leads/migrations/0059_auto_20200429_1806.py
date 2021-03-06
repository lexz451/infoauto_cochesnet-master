# Generated by Django 2.1 on 2020-04-29 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0058_auto_20200424_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicallead',
            name='result_error',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='result_error',
        ),
        migrations.AddField(
            model_name='historicallead',
            name='result_reason',
            field=models.CharField(blank=True, choices=[('rechaza_financiacion', 'Rechaza financiación'), ('rechaza_tasacion', 'Rechaza tasación'), ('rechaza_precio', 'Rechaza precio'), ('aplaza_compra', 'Aplaza compra'), ('compra_competencia', 'Compra competencia'), ('pre-reservado', 'Pre-Reservado'), ('reservado', 'Reservado'), ('publicidad', 'Publicidad'), ('otro_departamente', 'Otro Departamento'), ('error', 'Error')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='result_reason',
            field=models.CharField(blank=True, choices=[('rechaza_financiacion', 'Rechaza financiación'), ('rechaza_tasacion', 'Rechaza tasación'), ('rechaza_precio', 'Rechaza precio'), ('aplaza_compra', 'Aplaza compra'), ('compra_competencia', 'Compra competencia'), ('pre-reservado', 'Pre-Reservado'), ('reservado', 'Reservado'), ('publicidad', 'Publicidad'), ('otro_departamente', 'Otro Departamento'), ('error', 'Error')], max_length=255, null=True),
        ),
    ]
