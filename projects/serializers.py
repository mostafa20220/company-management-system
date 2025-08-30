from rest_framework import serializers
from .models import Project
from organizations.models import Employee

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the Project model."""

    class EmployeeBriefSerializer(serializers.ModelSerializer):
        full_name = serializers.CharField(source='user.get_full_name', read_only=True)
        class Meta:
            model = Employee
            fields = ('id', 'full_name', 'designation')

    assigned_employees_details = EmployeeBriefSerializer(source='assigned_employees', many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'start_date', 'end_date', 'company',
            'department', 'assigned_employees', 'assigned_employees_details'
        )
        # For write operations (POST, PUT), 'assigned_employees' will be a list of employee IDs.
        extra_kwargs = {
            'assigned_employees': {'write_only': True, 'queryset': Employee.objects.all()}
        }
