# Generated by Django 2.2 on 2020-07-23 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0081_auto_20200723_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicallead',
            name='result_reason',
            field=models.CharField(blank=True, choices=[('rechaza_financiacion', 'Rechaza financiación'), ('rechaza_tasacion', 'Rechaza tasación'), ('rechaza_precio', 'Rechaza precio'), ('aplaza_compra', 'Aplaza compra'), ('compra_competencia', 'Compra competencia'), ('compra_competencia_precio', 'Compra competencia por precio'), ('compra_competencia_proximidad', 'Compra competencia por proximidad'), ('compra_competencia_stock', 'Compra competencia por stock'), ('infinanciable', 'Infinanciable'), ('aplaza_decision', 'Aplaza decisión'), ('otro', 'Otro'), ('duplicado', 'Duplicado'), ('cita_cancelada', 'Cita cancelada'), ('informacion_cliente_incorrecta', 'Información cliente incorrecta'), ('ilocalizable', 'Ilocalizable'), ('disconforme_tasacion', 'Disconforme con tasación'), ('caducado', 'Caducado'), ('no_encaja_producto', 'No le encaja el producto'), ('no_encaja_precio', 'No le encaja el precio'), ('no_encaja_cuota', 'No le encaja la cuota'), ('vehiculo_ya_vendido', 'Vehiculo ya vendido'), ('caducado', 'Caducado'), ('pre-reservado', 'Pre-Reservado'), ('reservado', 'Reservado'), ('publicidad', 'Publicidad'), ('otro_departamento', 'Otro Departamento'), ('error', 'Error'), ('pedido', 'Pedido'), ('reservado', 'Reservado')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='result_reason',
            field=models.CharField(blank=True, choices=[('rechaza_financiacion', 'Rechaza financiación'), ('rechaza_tasacion', 'Rechaza tasación'), ('rechaza_precio', 'Rechaza precio'), ('aplaza_compra', 'Aplaza compra'), ('compra_competencia', 'Compra competencia'), ('compra_competencia_precio', 'Compra competencia por precio'), ('compra_competencia_proximidad', 'Compra competencia por proximidad'), ('compra_competencia_stock', 'Compra competencia por stock'), ('infinanciable', 'Infinanciable'), ('aplaza_decision', 'Aplaza decisión'), ('otro', 'Otro'), ('duplicado', 'Duplicado'), ('cita_cancelada', 'Cita cancelada'), ('informacion_cliente_incorrecta', 'Información cliente incorrecta'), ('ilocalizable', 'Ilocalizable'), ('disconforme_tasacion', 'Disconforme con tasación'), ('caducado', 'Caducado'), ('no_encaja_producto', 'No le encaja el producto'), ('no_encaja_precio', 'No le encaja el precio'), ('no_encaja_cuota', 'No le encaja la cuota'), ('vehiculo_ya_vendido', 'Vehiculo ya vendido'), ('caducado', 'Caducado'), ('pre-reservado', 'Pre-Reservado'), ('reservado', 'Reservado'), ('publicidad', 'Publicidad'), ('otro_departamento', 'Otro Departamento'), ('error', 'Error'), ('pedido', 'Pedido'), ('reservado', 'Reservado')], max_length=255, null=True),
        ),
    ]
