import django
from django.contrib.auth.views import LoginView
from django.urls import path
from dashboard import views as dashboard_views

urlpatterns = [
    path("",
        dashboard_views.DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        "export-csv-list/",
        dashboard_views.ExportCSVListView.as_view(),
        name="export_csv_list"
    ),
    path(
        "create-export-to-csv/",
        dashboard_views.CreateExportToCSVView.as_view(),
        name="create_export_to_csv"
    ),
    path(
        "create-schema/",
        dashboard_views.CreateSchemaView.as_view(),
        name="create_schema"
    )
]
