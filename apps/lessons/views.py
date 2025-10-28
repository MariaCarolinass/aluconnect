from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.lessons.models import Lesson
from apps.lessons.serializers import LessonSerializer
from apps.lessons.services.lessonService import course_has_minimum_lessons
from apps.lessons.serializers import LessonSerializer
from django.shortcuts import get_object_or_404
from apps.courses.models import Course

class LessonCreateView(APIView):
    """
    Cria uma nova aula associada a um curso específico.
    Requer autenticação.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        data = request.data.copy()
        data['course'] = course_id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonListView(APIView):
    """
    Lista todas as aulas de um curso.
    Acesso público.
    """
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def get(self, request, course_id):
        lessons = Lesson.objects.filter(course_id=course_id)
        serializer = self.serializer_class(lessons, many=True)
        return Response(serializer.data)


class LessonDetailView(APIView):
    """
    Retorna os detalhes de uma aula específica.
    Acesso público.
    """
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def get(self, request, course_id, lesson_id):
        lesson = get_object_or_404(Lesson, course_id=course_id, id=lesson_id)
        serializer = self.serializer_class(lesson)
        return Response(serializer.data)


class LessonUpdateView(APIView):
    """
    Atualiza os dados de uma aula específica.
    Requer autenticação.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, course_id, lesson_id):
        lesson = get_object_or_404(Lesson, course_id=course_id, id=lesson_id)
        serializer = self.serializer_class(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDeleteView(APIView):
    """
    Exclui uma aula de um curso, respeitando a regra de mínimo de aulas.
    Requer autenticação.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id, lesson_id):
        lesson = get_object_or_404(Lesson, course_id=course_id, id=lesson_id)
        
        if not course_has_minimum_lessons(lesson.course, minimum=2):
            return Response(
                {"error": "Curso precisa ter ao menos uma aula."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
