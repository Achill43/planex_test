import csv
import datetime

from django import forms
from django.conf import settings
from django.core.files import File
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets

from dashboard.tasks import schema_export_to_csv

from dashboard.models import Schema, ExportToCSV

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
        }
    ))

class SchemaForm(forms.ModelForm):

    class Meta:
        model = Schema
        fields = (
            'user', 'full_name', 'job', 'email', 'domain_name', 'phone',
            'company_name', 'text', 'integer', 'address', 'date'
        )
        widgets = {
            'user': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(SchemaForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update(
                    {"class": 'form-control'}
                )

class ExportToCSVForm(forms.Form):
    schemas_objects = forms.ModelMultipleChoiceField(
        queryset=Schema.objects.all(), widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'hidden-input'
            }
        )
    )
    full_name = forms.BooleanField(label="Full name", required=False)
    job = forms.BooleanField(label="job", required=False)
    email = forms.BooleanField(label="Email", required=False)
    domain_name = forms.BooleanField(label="Domain name", required=False)
    phone = forms.BooleanField(label="Phone", required=False)
    company_name = forms.BooleanField(label="Company name", required=False)
    text = forms.BooleanField(label="Text", required=False)
    integer = forms.BooleanField(label="Integer", required=False)
    address = forms.BooleanField(label="Address", required=False)
    date = forms.BooleanField(label="Date", required=False)

    def save(self, user):
        data = self.cleaned_data
        field_list = []
        if data['full_name']:
            field_list.append("full_name")
        if data['job']:
            field_list.append("job")
        if data['email']:
            field_list.append("email")
        if data['domain_name']:
            field_list.append("domain_name")
        if data['phone']:
            field_list.append("phone")
        if data['company_name']:
            field_list.append("company_name")
        if data['text']:
            field_list.append("text")
        if data['integer']:
            field_list.append("integer")
        if data['address']:
            field_list.append("address")
        if data['date']:
            field_list.append("date")
        
        curr_date = datetime.date.today()
        file_name = str(settings.STATICFILES_DIRS[0]) + "/csv/" + str(
            user.username) + str(
            curr_date) + ".csv"
        with open(file_name, 'w', encoding='UTF8') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(field_list)
            csvFile.close()
            export_to_csv_obj = ExportToCSV.objects.create(
                user=user,
            )
            upload_file_name = str(user.username) + str(curr_date) + ".csv"
            export_to_csv_obj.csv_file.save(upload_file_name, File(
                open(file_name)))
            export_to_csv_obj.save()

        schema_ids = list(data["schemas_objects"].values_list('id', flat=True))
        schema_export_to_csv.delay(
            export_to_csv_obj.id, field_list, schema_ids)
        return export_to_csv_obj
