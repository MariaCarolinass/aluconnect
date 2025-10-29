from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from apps.progress.models import Progress
from apps.progress.serializers import ProgressSerializer
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.users.constants import UserRole
from rest_framework.exceptions import PermissionDenied
from apps.certificates.tasks import generate_certificate
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Registro de Progresso",
    description="Marca uma aula como concluída para o aluno autenticado.",
    request=ProgressSerializer,
    responses={200: ProgressSerializer()},
    tags=["progress"],
)
class RegisterProgressView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgressSerializer 

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, course_id, lesson_id):
        student = request.user
        course = get_object_or_404(Course, id=course_id)
        lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

        total_lessons = course.lessons.count()
        completed_lessons = Progress.objects.filter(
            student=student, course=course, status='COMPLETED'
        ).count()

        if completed_lessons >= total_lessons:
            return Response(
                {"detail": "Curso já concluído. Progresso não pode ser alterado."},
                status=status.HTTP_403_FORBIDDEN
            )

        progress, created = Progress.objects.get_or_create(
            student=student,
            course=course,
            lesson=lesson,
            defaults={'status': 'COMPLETED'}
        )

        if not created and progress.status == 'COMPLETED':
            return Response(
                {"detail": "Aula já marcada como concluída."},
                status=status.HTTP_200_OK
            )

        progress.status = 'COMPLETED'
        progress.save()

        updated_completed = Progress.objects.filter(
            student=student, course=course, status='COMPLETED'
        ).count()

        if updated_completed == total_lessons:
            generate_certificate.delay(student.id, course.id)

        serializer = self.get_serializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@extend_schema(
    summary="Progresso do Aluno",
    description="Lista o progresso geral de um aluno.",
    responses={200: ProgressSerializer(many=True)},
    tags=["progress"],
)
class ProgressListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgressSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role != UserRole.STUDENT:
            raise PermissionDenied("Apenas estudantes podem ver seu progresso.")
        return Progress.objects.filter(student=user)


@extend_schema(
    summary="Progresso do Aluno em Curso",
    description="Lista o progresso de um aluno em um curso específico.",
    responses={200: ProgressSerializer(many=True)},
    tags=["progress"],
)
class CourseProgressView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgressSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role != UserRole.STUDENT:
            raise PermissionDenied("Apenas estudantes podem ver seu progresso.")
        course_id = self.kwargs.get('course_id')
        return Progress.objects.filter(student=user, course_id=course_id)