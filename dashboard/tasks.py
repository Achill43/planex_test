import csv
from planex_test.celery import app

from dashboard.models import ExportToCSV, Schema

@app.task
def schema_export_to_csv(export_to_csv_id, fields_list, schema_ids):
    export_to_csv_obj = ExportToCSV.objects.get(id=export_to_csv_id)
    export_to_csv_obj.set_in_progress()
    schema_qs = Schema.objects.filter(id__in=schema_ids)
    with open(str(export_to_csv_obj.csv_file.path), 'w', encoding='UTF8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(fields_list)
        for schema_item in schema_qs:
            row = []
            if "full_name" in fields_list:
                row.append(schema_item.full_name)
            if 'job' in fields_list:
                row.append(schema_item.job)
            if'email' in fields_list:
                row.append(schema_item.email)
            if 'domain_name' in fields_list:
                row.append(schema_item.domain_name)
            if 'phone' in fields_list:
                row.append(schema_item.phone)
            if 'company_name' in fields_list:
                row.append(schema_item.company_name)
            if 'text' in fields_list:
                row.append(schema_item.text)
            if 'integer' in fields_list:
                row.append(schema_item.integer)
            if 'address' in fields_list:
                row.append(schema_item.address)
            if 'date' in fields_list:
                row.append(schema_item.date)
            print(row)
            writer.writerow(row)

        csvFile.close()
    export_to_csv_obj.set_success()
