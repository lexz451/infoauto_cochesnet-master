# Generated by Django 2.1 on 2020-04-24 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0056_auto_20200423_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltask',
            name='type',
            field=models.CharField(choices=[('date', 'Visita / Test Drive'), ('appraisal', 'Appraisal'), ('budget', 'Budget'), ('financing', 'Financing'), ('warranty', 'Warranty'), ('vehicle_information', 'Vehicle information'), ('response_information_mail', 'Respuesta a solicitud vía Email'), ('pending_assignment', 'Pendiente de asignación'), ('lost_call', 'Atender una llamada perdida'), ('send_email', 'Enviar email'), ('workshop_appointment', 'Cita para taller'), ('other', 'Otros')], max_length=255),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('date', 'Visita / Test Drive'), ('appraisal', 'Appraisal'), ('budget', 'Budget'), ('financing', 'Financing'), ('warranty', 'Warranty'), ('vehicle_information', 'Vehicle information'), ('response_information_mail', 'Respuesta a solicitud vía Email'), ('pending_assignment', 'Pendiente de asignación'), ('lost_call', 'Atender una llamada perdida'), ('send_email', 'Enviar email'), ('workshop_appointment', 'Cita para taller'), ('other', 'Otros')], max_length=255),
        ),
    ]
