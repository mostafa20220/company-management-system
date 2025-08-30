from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN)

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role ==User.Role.MANAGER)

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.EMPLOYEE)

class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsOwnerOrManagerOrAdmin(BasePermission):
    """
    Object-level permission to only allow owners of an object, their manager, or an admin to edit it.
    Assumes the model instance has an `employee` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the employee themselves, their manager, or an admin.
        is_admin = request.user.role == User.Role.ADMIN
        is_manager = request.user.role == User.Role.MANAGER and obj.employee.department == request.user.employee.department
        is_owner = obj.employee.user == request.user

        return is_admin or is_manager or is_owner
