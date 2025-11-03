import pytest
from apps.lessons.services.lessonService import course_has_minimum_lessons
from apps.lessons.models import Lesson
from apps.courses.models import Course


@pytest.mark.django_db
class TestLessonService:

    def setup_method(self):
        self.course = Course.objects.create(title="Curso Teste")

    def test_course_has_minimum_lessons_true(self):
        Lesson.objects.create(course=self.course, title="Aula 1", order=1)
        assert course_has_minimum_lessons(self.course, minimum=1) is True

    def test_course_has_minimum_lessons_false(self):
        assert course_has_minimum_lessons(self.course, minimum=1) is False
