# Generated by Django 2.1 on 2020-05-05 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0064_auto_20200505_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='leads.Lead'),
        ),
    ]
