from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, FormView
from django.urls import reverse

from dashboard.forms import UserLoginForm, SchemaForm, ExportToCSVForm
from dashboard.models import Schema, ExportToCSV


class UserLoginView(LoginView):
    template_name = 'dashboard/login_form.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse('dashboard')

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'
    context_object_name = "schemas"

    def get_queryset(self):
        user = self.request.user
        qs = Schema.objects.filter(user=user)
        return qs

class CreateSchemaView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/create_schema.html'
    form_class = SchemaForm
    success_url = "/dashboard/"

    def get_initial(self):
        data_dict = {
            'user': self.request.user,
        }
        return data_dict

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class ExportCSVListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/export_csv_list.html'

    def get_queryset(self):
        user = self.request.user
        qs = ExportToCSV.objects.filter(user=user)
        return qs


class CreateExportToCSVView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/create_export_to_csv.html'
    form_class = ExportToCSVForm
    success_url = "/dashboard/export-csv-list/"

    def get_initial(self):
        schema_ids = self.request.GET.getlist("schema_ids[]")
        data_dict = {}
        if schema_ids:
            data_dict = {
                'schemas_objects': Schema.objects.filter(id__in=schema_ids),
            }
        return data_dict

    def form_valid(self, form):
        user = self.request.user
        form.save(user=user)
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    template_name=self.template_name,
                    context=self.get_context_data(),
                    request=request
                ),
            }
            return JsonResponse(data)
        return super(CreateExportToCSVView, self).get(request, *args, **kwargs)