from django.db import models
from organizations.models import Employee, Department, Company
from companyManagementSystem.models import TimeBaseModel

class Project(TimeBaseModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    company = models.ForeignKey(Company, related_name='projects', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='projects', on_delete=models.CASCADE)

    assigned_employees = models.ManyToManyField(Employee, related_name='projects', blank=True)

    def __str__(self):
        return self.name
