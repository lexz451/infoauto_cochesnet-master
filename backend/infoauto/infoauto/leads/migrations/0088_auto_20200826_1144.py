# Generated by Django 2.2 on 2020-08-26 09:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0087_auto_20200826_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('custom_id', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BusinessPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('custom_id', models.PositiveIntegerField()),
                ('activity', models.CharField(max_length=256)),
                ('position', models.CharField(max_length=256, null=True)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='leads.Sector')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='client',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='leads.BusinessPosition'),
        ),
        migrations.AddField(
            model_name='historicalclient',
            name='position',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='leads.BusinessPosition'),
        ),
    ]
