from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Project

@receiver(post_save, sender=Project)
def increment_project_count(sender, instance, created, **kwargs):
    """
    When a new Project is created, increment the project counters on the
    related Company and Department.
    """
    if created:
        instance.company.number_of_projects = F('number_of_projects') + 1
        instance.department.number_of_projects = F('number_of_projects') + 1
        instance.company.save(update_fields=['number_of_projects'])
        instance.department.save(update_fields=['number_of_projects'])

@receiver(post_delete, sender=Project)
def decrement_project_count(sender, instance, **kwargs):
    """
    When a Project is deleted, decrement the project counters on the
    related Company and Department.
    """
    instance.company.number_of_projects = F('number_of_projects') - 1
    instance.department.number_of_projects = F('number_of_projects') - 1
    instance.company.save(update_fields=['number_of_projects'])
    instance.department.save(update_fields=['number_of_projects'])
