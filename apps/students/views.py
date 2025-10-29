from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from apps.users.constants import UserRole
from apps.students.models import Student
from apps.students.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status


class StudentListView(generics.ListAPIView):
    """
    Lista todos os usuários com papel de estudante.
    Requer autenticação.
    """
    queryset = Student.objects.filter(user__role=UserRole.STUDENT)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentDetailView(generics.RetrieveAPIView):
    """
    Retorna os detalhes de um estudante específico.
    Requer autenticação.
    """
    queryset = Student.objects.filter(user__role=UserRole.STUDENT)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class StudentCreateView(generics.CreateAPIView):
    """
    Cria um novo usuário com papel de estudante.
    Requer autenticação de administrador.
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role != UserRole.ADMIN:
            raise PermissionDenied("Você não tem permissão para criar estudantes.")

        self.instance = serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método 'create' apenas para personalizar a resposta JSON.
        """
        response = super().create(request, *args, **kwargs)
        user = getattr(self, 'instance', None)

        return Response(
            {
                "success": True,
                "message": f"Usuário '{user.role}' criado com sucesso!",
                "data": response.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {
                    "success": False,
                    "error": str(exc),
                    "detail": "Você não tem permissão para realizar essa ação."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().handle_exception(exc)


class StudentUpdateView(generics.UpdateAPIView):
    """
    Atualiza os dados de um estudante.
    Requer autenticação.
    """
    queryset = Student.objects.filter(user__role=UserRole.STUDENT)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
