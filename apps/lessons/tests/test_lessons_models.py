import pytest
from apps.courses.models import Course
from apps.lessons.models import Lesson


@pytest.mark.django_db
class TestLessonModel:
    
    def test_create_lesson(self):
        course = Course.objects.create(title="Curso de Django")
        lesson = Lesson.objects.create(course=course, title="Aula 1", order=1)
        assert lesson.title == "Aula 1"
        assert lesson.course == course
        assert str(lesson) == f"Aula: {lesson.title}"

    def test_lessons_ordering(self):
        course = Course.objects.create(title="Curso com aulas")
        Lesson.objects.create(course=course, title="Aula 1", order=1)
        Lesson.objects.create(course=course, title="Aula 2", order=2)
        lessons = Lesson.objects.filter(course=course).order_by("order")
        assert lessons[0].title == "Aula 1"
        assert lessons[1].title == "Aula 2"
