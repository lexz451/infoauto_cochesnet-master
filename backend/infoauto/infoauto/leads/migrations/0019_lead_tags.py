# Generated by Django 2.1 on 2019-01-24 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags_app', '0001_initial'),
        ('leads', '0018_auto_20190123_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tags_app.Tag'),
        ),
    ]
