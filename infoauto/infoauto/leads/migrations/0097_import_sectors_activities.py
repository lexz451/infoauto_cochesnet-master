import os
from django.db import migrations
import openpyxl


def insert_sectors(apps, schema_editor):

	Sector = apps.get_model('leads', 'Sector')
	BusinessActivity = apps.get_model('leads', 'BusinessActivity')

	excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', "MAESTRO_ACTIVIDADES,_SECTORES_.xlsx")

	xlsx_file = excel_path
	wb_obj = openpyxl.load_workbook(xlsx_file)

	# Obtenemos el archivo
	if wb_obj:
		sheet = wb_obj.active

		for row in sheet.iter_rows(min_row=2):
			print(row[0].value)
			print(row[2].value)
			print(row[3].value)
			print(row[4].value)
			print("*" * 50)

			if row[0].value and row[2].value and row[3].value and row[4].value:  # Null cells filtered
				sector_data = {
					"name": row[4].value
				}

				sector, created = Sector.objects.get_or_create(custom_id=row[3].value, defaults=sector_data)

				position_data = {
					"sector": sector
				}
				business_position = BusinessActivity.objects.get_or_create(custom_id=row[0].value, activity=row[2].value, defaults=position_data)
				if not business_position:
					return None


class Migration(migrations.Migration):

	dependencies = [
		('leads', '0096_auto_20200901_1108'),
	]

	operations = [
		migrations.RunPython(insert_sectors),
	]
