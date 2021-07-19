from datetime import date

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Schema(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User")
    full_name = models.CharField(max_length=150, verbose_name="Full name")
    job = models.CharField(max_length=100, verbose_name="Job")
    email = models.CharField(max_length=150, verbose_name="E-mail")
    domain_name = models.CharField(max_length=100, verbose_name="Domain name")
    phone = models.CharField(max_length=20, verbose_name="Phone number")
    company_name = models.CharField(
        max_length=150, verbose_name="Company name")
    text = models.TextField(verbose_name="Text")
    integer = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(1000), MinValueValidator(1)],
        verbose_name="Integer"
    )
    address = models.CharField(max_length=255, verbose_name="Address")
    date = models.DateField(default=date.today, verbose_name="Date")

    class Meta:
        verbose_name = "Schemas"
        verbose_name_plural = "Schema"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.full_name} - {self.job}"


NEW = 'NEW'
SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
PROGRESS = "PROGRESS"

IMPORT_STATE_CHOICES = (
    (NEW, "New"),
    (SUCCESS, "Success"),
    (FAILURE, "Failure"),
    (PROGRESS, "In progress")
)


class ExportToCSV(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User")
    status = models.CharField(
        max_length=8, choices=IMPORT_STATE_CHOICES, default=NEW)
    csv_file = models.FileField(
        upload_to='export/csv/%Y/%m/%d',
        blank=True, null=True, verbose_name="CSV file")
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = "Export to CSV"
        verbose_name_plural = "Exports to CSV"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.status} - {self.csv_file}"

    def set_in_progress(self):
        self.status = PROGRESS
        self.save()

    def set_error(self):
        self.status = FAILURE
        self.save()

    def set_success(self):
        self.status = SUCCESS
        self.save()
