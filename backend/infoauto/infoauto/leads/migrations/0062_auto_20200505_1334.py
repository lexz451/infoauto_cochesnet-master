# Generated by Django 2.1 on 2020-05-05 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0061_leadmanagement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadmanagement',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_managements', to='leads.Lead'),
        ),
    ]
