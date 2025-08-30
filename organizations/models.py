from django.db import models
from django.conf import settings
from django.utils import timezone

from companyManagementSystem.models import TimeBaseModel


class Company(TimeBaseModel):
    name = models.CharField(max_length=255, unique=True)

    number_of_departments = models.PositiveIntegerField(default=0)
    number_of_employees = models.PositiveIntegerField(default=0)
    number_of_projects = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

class Department(TimeBaseModel):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)

    number_of_employees = models.PositiveIntegerField(default=0)
    number_of_projects = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'company'], name='unique_department_per_company')
        ]

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Employee(TimeBaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee')
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    designation = models.CharField(max_length=100)
    hired_on = models.DateField(null=True, blank=True)

    @property
    def days_employed(self):
        if self.hired_on:
            return (timezone.now().date() - self.hired_on).days
        return 0

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"
