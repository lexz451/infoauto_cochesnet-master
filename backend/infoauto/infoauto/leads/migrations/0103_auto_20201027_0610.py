# Generated by Django 2.2 on 2020-10-27 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0102_auto_20201026_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadmanagement',
            name='event',
            field=models.CharField(blank=True, choices=[('lead_not_attended', 'Lead no atendido'), ('lead_attended', 'Lead atendido'), ('lead_end', 'Lead finalizado'), ('lead_create_task', 'Nueva tarea creada en lead'), ('lead_done_task', 'Tarea finalizada en lead'), ('lead_create_traking', 'Nuevo seguimiento en lead'), ('lead_done_traking', 'Seguimiento finalizado en lead'), ('incoming_all', 'Llamada entrante en lead'), ('outcomming_all', 'Llamada saliente en lead'), ('outcomming_all', 'Whatsapp enviado')], max_length=224, null=True),
        ),
    ]
