from django.contrib.auth.models import AbstractUser
from django.db import models
from companyManagementSystem.models import TimeBaseModel

class User(TimeBaseModel, AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        EMPLOYEE = "EMPLOYEE", "Employee"

    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(max_length=50, choices=Role.choices)

    # Set email as the main username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        full_name = f"{self.username}".strip()
        return full_name if full_name else self.email