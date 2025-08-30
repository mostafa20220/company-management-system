from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Department, Employee

# --- Department Counter Signals ---

@receiver(post_save, sender=Department)
def increment_department_count(sender, instance, created, **kwargs):
    if created:
        instance.company.number_of_departments = F('number_of_departments') + 1
        instance.company.save(update_fields=['number_of_departments'])

@receiver(post_delete, sender=Department)
def decrement_department_count(sender, instance, **kwargs):
    instance.company.number_of_departments = F('number_of_departments') - 1
    instance.company.save(update_fields=['number_of_departments'])


@receiver(post_save, sender=Employee)
def handle_employee_save(sender, instance, created, **kwargs):
    """
    Handles logic when an Employee is created or its department changes.
    """
    if created:
        # New employee is created
        instance.company.number_of_employees = F('number_of_employees') + 1
        instance.department.number_of_employees = F('number_of_employees') + 1
        instance.company.save(update_fields=['number_of_employees'])
        instance.department.save(update_fields=['number_of_employees'])
    else:
        # Check if the department was changed on an existing employee
        try:
            old_instance = Employee.objects.get(pk=instance.pk)
            if old_instance.department != instance.department:
                # Department has changed, decrement old and increment new
                old_instance.department.number_of_employees = F('number_of_employees') - 1
                instance.department.number_of_employees = F('number_of_employees') + 1
                old_instance.department.save(update_fields=['number_of_employees'])
                instance.department.save(update_fields=['number_of_employees'])
        except Employee.DoesNotExist:
            # This case can be ignored as it means the object is being created
            pass


@receiver(post_delete, sender=Employee)
def decrement_employee_count(sender, instance, **kwargs):
    instance.company.number_of_employees = F('number_of_employees') - 1
    instance.department.number_of_employees = F('number_of_employees') - 1
    instance.company.save(update_fields=['number_of_employees'])
    instance.department.save(update_fields=['number_of_employees'])
