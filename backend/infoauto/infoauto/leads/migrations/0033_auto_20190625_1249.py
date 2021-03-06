# Generated by Django 2.1 on 2019-06-25 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('source_channels', '0003_auto_20190128_1116'),
        ('leads', '0032_auto_20190618_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvehicle',
            name='lead',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='leads.Lead'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='media',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='source_channels.Channel'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='origin',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='leads.Origin'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='leads.Lead'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to='source_channels.Channel'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to='leads.Origin'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='leads.Vehicle'),
        )
    ]
