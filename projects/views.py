
from rest_framework import viewsets, permissions

from users.models import User
from .models import Project
from .serializers import ProjectSerializer
from users.permissions import IsManager, IsAdmin

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    Creation, update, and deletion are restricted to Managers and Admins.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Allow any authenticated user to view, but only managers or admins to modify.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsManager | IsAdmin]
        return super().get_permissions()

    def get_queryset(self):
        """
        Restrict the queryset for non-admin users.
        - Managers see projects in their department.
        - Employees see projects they are assigned to.
        """
        user = self.request.user
        if user.role == User.Role.MANAGER:
            try:
                manager_department = user.employee.department
                return Project.objects.filter(department=manager_department)
            except:
                return Project.objects.none()
        elif user.role == User.Role.EMPLOYEE:
            try:
                return user.employee.projects.all()
            except:
                return Project.objects.none()

        # Admins can see all projects.
        return super().get_queryset()
