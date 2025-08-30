# This file is now deprecated. Use companyManagementSystem.models.TimeBaseModel instead.

from django.db import models

class TimeBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
