from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import User
from .models import Company, Department, Employee
from .serializers import CompanySerializer, DepartmentSerializer, EmployeeSerializer
from users.permissions import IsAdmin, IsReadOnly, IsManager

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    Only Admins can create, update, or delete companies.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdmin | IsReadOnly]

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows departments to be viewed or edited.
    Only Admins can create, update, or delete departments.
    Managers can view departments.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdmin | IsReadOnly]

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    Admins and Managers can create employees.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - POST (create) is restricted to Admins and Managers.
        - Other actions (list, retrieve, update, delete) use default IsAuthenticated.
        """
        if self.action == 'create':
            self.permission_classes = [IsManager | IsAdmin]
        return super().get_permissions()

    def get_queryset(self):
        """
        Optionally restricts the returned employees, returning only employees
        in the same department for a manager.
        """
        user = self.request.user
        if user.role == User.Role.MANAGER:
            try:
                manager_department = user.employee.department
                return Employee.objects.filter(department=manager_department)
            except Employee.DoesNotExist:
                # If the manager is not linked to an employee profile, return none.
                return Employee.objects.none()
        elif user.role == User.Role.EMPLOYEE:
            return Employee.objects.filter(user=user)

        return super().get_queryset()
