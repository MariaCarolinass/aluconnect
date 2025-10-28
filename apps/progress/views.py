from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.progress.models import Progress
from apps.progress.serializers import ProgressSerializer
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.certificates.tasks import generate_certificate
from django.shortcuts import get_object_or_404


class RegisterProgressView(APIView):
    """
    Marca uma aula como concluída para o aluno autenticado.
    Gera certificado automaticamente ao concluir todas as aulas.
    """
    permission_classes = [IsAuthenticated]

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

        serializer = ProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ProgressListView(APIView):
    """
    Lista o progresso geral de um aluno.
    Requer autenticação.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        progress = Progress.objects.filter(student__id=student_id)
        serializer = ProgressSerializer(progress, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseProgressView(APIView):
    """
    Lista o progresso de um aluno em um curso específico.
    Requer autenticação.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, course_id):
        progress = Progress.objects.filter(
            student__id=student_id,
            course__id=course_id
        )
        serializer = ProgressSerializer(progress, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)