from django.contrib import admin

from dashboard.models import Schema, ExportToCSV

@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name']
    list_filter = ['user']

@admin.register(ExportToCSV)
class ExportToCSV(admin.ModelAdmin):
    list_display = ['user', 'csv_file', 'status']
    list_filter = ['user', 'status']
