from django.db import migrations
import os
import csv

def update_postal_codes(apps, schema_editor):

    Locality = apps.get_model('countries', 'Locality')
    PostalCode = apps.get_model('countries', 'PostalCode')

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', "municipios.csv")
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            postal_code_number = row[0]
            locality_name = row[1]

            localities = Locality.objects.filter(name=locality_name, province__country=28)
            for locality in localities:
                PostalCode.objects.create(locality=locality, postal_code_number=postal_code_number)


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0008_postalcode'),
    ]

    operations = [
        migrations.RunPython(update_postal_codes),
    ]
