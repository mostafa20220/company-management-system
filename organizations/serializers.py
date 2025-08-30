from rest_framework import serializers
from .models import Company, Department, Employee
from users.serializers import UserSerializer

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'number_of_departments', 'number_of_employees', 'number_of_projects')
        read_only_fields = ('number_of_departments', 'number_of_employees', 'number_of_projects')

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name', 'company', 'number_of_employees', 'number_of_projects')
        read_only_fields = ('number_of_employees', 'number_of_projects')

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'user', 'company', 'department', 'mobile_number', 'address', 'designation', 'hired_on', 'days_employed')
        read_only_fields = ('days_employed',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            # Update the nested User object.
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        return super().update(instance, validated_data)

