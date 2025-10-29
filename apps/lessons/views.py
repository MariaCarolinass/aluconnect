from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.lessons.serializers import LessonSerializer
from apps.lessons.services.lessonService import course_has_minimum_lessons
from apps.users.constants import UserRole
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse


def _ensure_course_permission(user, course):
    """
    Garante que apenas instrutores do curso ou administradores possam modificá-lo.
    """
    if user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise PermissionDenied("Apenas instrutores podem modificar aulas.")
    if user.role == UserRole.INSTRUCTOR and user not in course.instructors.all():
        raise PermissionDenied("Você não é o instrutor deste curso.")
    

@extend_schema(
    summary="Criação de aula",
    description="Permite que um instrutor crie uma nova aula associada a um curso específico.",
    request=LessonSerializer,
    responses={
        201: OpenApiResponse(description="Aula criada com sucesso."),
        403: OpenApiResponse(description="Permissão negada."),
        400: OpenApiResponse(description="Dados inválidos para criação da aula."),
    },
    tags=["lessons"],
    examples=[
        OpenApiExample(
            "Exemplo de Criação de Aula",
            value={"title": "Aula 1: Introdução", "content": "Conteúdo da aula 1."},
            request_only=True,
        )
    ],
)
class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        _ensure_course_permission(self.request.user, course)
        serializer.save(course=course)


@extend_schema(
    summary="Listagem de aulas do curso",
    description="Lista todas as aulas pertencentes a um curso específico.",
    responses={200: LessonSerializer(many=True)},
    tags=["lessons"],
)
class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id).order_by('id')


@extend_schema(
    summary="Detalhes da aula",
    description="Retorna os detalhes de uma aula específica de um curso.",
    responses={200: LessonSerializer()},
    tags=["lessons"],
)
class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    lookup_field = "lesson_id"

    def get_object(self):
        return get_object_or_404(
            Lesson,
            course_id=self.kwargs["course_id"],
            id=self.kwargs["lesson_id"],
        )


@extend_schema(
    summary="Atualização de aula",
    description="Permite que um instrutor atualize os dados de uma aula específica de seu curso.",
    request=LessonSerializer,
    responses={
        200: OpenApiResponse(description="Aula atualizada com sucesso."),
        403: OpenApiResponse(description="Permissão negada."),
    },
    tags=["lessons"],
)
class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "lesson_id"

    def get_object(self):
        lesson = get_object_or_404(
            Lesson,
            course_id=self.kwargs["course_id"],
            id=self.kwargs["lesson_id"],
        )
        _ensure_course_permission(self.request.user, lesson.course)
        return lesson


@extend_schema(
    summary="Exclusão de aula",
    description="Exclui uma aula de um curso, garantindo que o curso mantenha o número mínimo de aulas.",
    responses={
        204: OpenApiResponse(description="Aula excluída com sucesso."),
        400: OpenApiResponse(description="Curso precisa ter ao menos uma aula."),
        403: OpenApiResponse(description="Permissão negada."),
    },
    tags=["lessons"],
)
class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "lesson_id"

    def get_object(self):
        lesson = get_object_or_404(
            Lesson,
            course_id=self.kwargs["course_id"],
            id=self.kwargs["lesson_id"],
        )
        _ensure_course_permission(self.request.user, lesson.course)
        return lesson

    def perform_destroy(self, instance):
        if not course_has_minimum_lessons(instance.course, minimum=2):
            raise PermissionDenied("Curso precisa ter ao menos uma aula.")
        instance.delete()

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)

    