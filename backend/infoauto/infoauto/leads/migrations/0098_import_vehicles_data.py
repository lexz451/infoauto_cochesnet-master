from django.db import migrations
import os
import openpyxl


def insert_vehicles_data(apps, schema_editor):

	VehicleBrand = apps.get_model('leads', 'VehicleBrand')
	VehicleModel = apps.get_model('leads', 'VehicleModel')
	VehicleVersion = apps.get_model('leads', 'VehicleVersion')
	GasType = apps.get_model('leads', 'GasType' )

	excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', "MAESTRO_DE_MODELOS_MARCAS_Y_VERSIONES.xlsx")

	xlsx_file = excel_path
	wb_obj = openpyxl.load_workbook(xlsx_file)

	# Obtenemos el archivo
	if wb_obj:
		sheet = wb_obj.active

		for row in sheet.iter_rows(min_row=2):
				print("{} | {} | {} | {} | {} | {} | {}".format(row[0].value, row[1].value, row[2].value, row[3].value,
					row[4].value, row[5].value, row[6].value, row[7].value))
				print("*" * 50)

				brand, created = VehicleBrand.objects.get_or_create(name=row[0].value)

				model, created = VehicleModel.objects.get_or_create(model_name=row[1].value, defaults={"brand": brand})

				version_data = {
					"comments": row[8].value if row[8].value not in [None, ""] else "",
					"size": row[2].value,
				}
				if row[3].value and row[4].value and row[5].value and row[6].value and row[7].value:
					fuel = row[6].value
					gas_type = None

					if fuel:
						gas_type = GasType.objects.filter(name__icontains=fuel).first()

					vehicle_version, created = VehicleVersion.objects.get_or_create(
						version_name=row[3].value,
						motor=row[4].value,
						engine_power=int(row[5].value),
						fuel=fuel,
						gearbox=row[7].value,
						vehicle_model=model,
						gas_type=gas_type,
						defaults={**version_data}
					)

					if not vehicle_version:
						return


class Migration(migrations.Migration):

	dependencies = [
		('leads', '0097_import_sectors_activities'),
	]

	operations = [
		migrations.RunPython(insert_vehicles_data),
	]
