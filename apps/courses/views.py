from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer, CourseDetailSerializer
from apps.courses.permissions import IsInstructor


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para cursos (CRUD).
    Acesso restrito a instrutores.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsInstructor]


class CourseCreateView(generics.CreateAPIView):
    """
    Cria um novo curso.
    Requer autenticação.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.save()
        course.instructors.add(self.request.user)


class CourseListView(generics.ListAPIView):
    """
    Lista todos os cursos disponíveis.
    Acesso público.
    """
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]


class CourseDetailView(generics.RetrieveAPIView):
    """
    Retorna os detalhes de um curso específico.
    Acesso público.
    """
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'


class CourseUpdateView(generics.UpdateAPIView):
    """
    Atualiza os dados de um curso.
    Requer autenticação.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class EnrollStudentView(generics.GenericAPIView):
    """
    Inscreve o usuário autenticado em um curso.
    """
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        course.students.add(request.user)
        return Response({"detail": "Inscrição realizada com sucesso."}, status=status.HTTP_200_OK)


class StudentCoursesView(generics.ListAPIView):
    """
    Lista os cursos em que um aluno está matriculado.
    Requer autenticação.
    """
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['id']
        return Course.objects.filter(students__id=student_id)


class InstructorCoursesView(generics.ListAPIView):
    """
    Lista os cursos ministrados por um instrutor.
    Requer autenticação.
    """
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        instructor_id = self.kwargs['id']
        return Course.objects.filter(instructors__id=instructor_id)
