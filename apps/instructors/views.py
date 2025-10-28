from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.constants import UserRole
from apps.instructors.models import Instructor
from apps.instructors.serializers import InstructorSerializer
from rest_framework import status


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

    def post(self, request):
        user = request.user
        if user.role != UserRole.INSTRUCTOR:
            user.role = UserRole.INSTRUCTOR
            user.save()

        profile, created = Instructor.objects.get_or_create(user=user)
        serializer = self.get_serializer(profile)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class InstructorUpdateView(generics.UpdateAPIView):
    """
    Atualiza os dados do perfil de instrutor.
    Requer autenticação.
    """
    queryset = Instructor.objects.filter(user__role=UserRole.INSTRUCTOR)
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
