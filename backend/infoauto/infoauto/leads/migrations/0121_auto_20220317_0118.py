# Generated by Django 2.2 on 2022-03-17 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0120_campaign_concession_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='b_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='m_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='o_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='s_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='v_id',
            field=models.IntegerField(null=True),
        ),
    ]
