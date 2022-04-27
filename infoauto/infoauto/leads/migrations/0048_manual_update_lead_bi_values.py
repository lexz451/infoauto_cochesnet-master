
from django.db import migrations, models


def update_lead_bi_values(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('leads', '0047_auto_20191125_1653'),
    ]

    operations = [
        #migrations.RunPython(update_lead_bi_values),

    ]
