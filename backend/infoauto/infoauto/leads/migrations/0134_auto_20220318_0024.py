# Generated by Django 2.2 on 2022-03-17 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0133_auto_20220318_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='utm_id',
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaingId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
