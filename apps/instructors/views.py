from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from apps.users.constants import UserRole
from apps.instructors.models import Instructor
from apps.instructors.serializers import InstructorSerializer


class InstructorListView(generics.ListAPIView):
    """
    Lista todos os perfis de instrutores.
    Requer autenticação.
    """
    queryset = Instructor.objects.filter(user__role=UserRole.INSTRUCTOR)
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]


class InstructorDetailView(generics.RetrieveAPIView):
    """
    Retorna os detalhes de um instrutor específico.
    Requer autenticação.
    """
    queryset = Instructor.objects.filter(user__role=UserRole.INSTRUCTOR)
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class InstructorCreateView(generics.CreateAPIView):
    """
    Cria ou retorna o perfil de instrutor do usuário autenticado.
    Atualiza o papel do usuário para INSTRUCTOR.
    """
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user

        if user.role != UserRole.ADMIN:
            raise PermissionDenied("Você não tem permissão para criar instrutores.")

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

class InstructorUpdateView(generics.UpdateAPIView):
    """
    Atualiza os dados do perfil de instrutor.
    Requer autenticação.
    """
    queryset = Instructor.objects.filter(user__role=UserRole.INSTRUCTOR)
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
