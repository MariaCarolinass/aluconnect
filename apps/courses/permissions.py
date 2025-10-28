from rest_framework.permissions import BasePermission
from apps.users.constants import UserRole


class IsInstructor(BasePermission):
    """
    Permissão que permite acesso apenas a usuários com papel de INSTRUCTOR.
    """

    message = "Apenas instrutores podem acessar este recurso."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.INSTRUCTOR)