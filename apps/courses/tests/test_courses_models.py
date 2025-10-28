import pytest
from apps.courses.models import Course
from apps.lessons.models import Lesson


@pytest.mark.django_db
class TestCourseModel:

    def test_create_course(self):
        course = Course.objects.create(title="Curso de Django")
        assert course.title == "Curso de Django"
        assert str(course) == f"Curso: {course.title}"

    def test_cannot_delete_course_with_lessons(self):
        course = Course.objects.create(title="Curso com aulas")
        Lesson.objects.create(course=course, title="Aula 1", order=1)

        course.delete()
        assert not Course.objects.filter(id=course.id).exists()