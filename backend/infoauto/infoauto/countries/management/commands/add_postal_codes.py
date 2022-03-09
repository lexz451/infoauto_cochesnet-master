from django.core.management.base import BaseCommand
import os
import csv
from tqdm import tqdm
from infoauto.countries.models import Locality, PostalCode


class Command(BaseCommand):
    help = "Realiza una carga de códigos postales"

    def handle(self, *args, **options):
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', "municipios.csv")
        with open(csv_path) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = sum(1 for row in csv_reader)
            csv_file.seek(0)
            n, i = 0, 0

            with tqdm(total=row_count) as pbar:
                for row in csv_reader:
                    postal_code_number = row[0]
                    locality_name = row[1]
                    i += 1

                    localities = Locality.objects.filter(name=locality_name, province__country=28)
                    for locality in localities:
                        PostalCode.objects.create(locality=locality, postal_code_number=postal_code_number)
                        n += 1

                    pbar.update(1)

        description = "Processed {0} / {1} localities".format(i, row_count)
        self.stdout.write(self.style.SUCCESS(description))