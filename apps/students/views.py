from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.models import User
from apps.users.constants import UserRole
from apps.students.serializers import StudentSerializer


class StudentListView(generics.ListAPIView):
    """
    Lista todos os usuários com papel de estudante.
    Requer autenticação.
    """
    queryset = User.objects.filter(role=UserRole.STUDENT)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentDetailView(generics.RetrieveAPIView):
    """
    Retorna os detalhes de um estudante específico.
    Requer autenticação.
    """
    queryset = User.objects.filter(role=UserRole.STUDENT)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class StudentCreateView(generics.CreateAPIView):
    """
    Cria um novo usuário com papel de estudante.
    Requer autenticação.
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            existing_user = User.objects.get(email=serializer.validated_data['email'])
            if existing_user.role != UserRole.STUDENT:
                raise ValueError("A user with this email already exists with a different role.")
            return existing_user
        except User.DoesNotExist:
            pass
        serializer.save(role=UserRole.STUDENT)


class StudentUpdateView(generics.UpdateAPIView):
    """
    Atualiza os dados de um estudante.
    Requer autenticação.
    """
    queryset = User.objects.filter(role=UserRole.STUDENT)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
