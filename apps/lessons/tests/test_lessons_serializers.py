import pytest
from apps.lessons.serializers import LessonSerializer
from apps.lessons.models import Lesson
from apps.courses.models import Course


@pytest.mark.django_db
class TestLessonSerializer:

    def setup_method(self):
        self.course = Course.objects.create(title="Curso Teste")

    def test_validate_unique_order(self):
        Lesson.objects.create(course=self.course, title="Aula 1", order=1)
        data = {"title": "Aula 2", "order": 1}
        serializer = LessonSerializer(data=data, context={"course": self.course})
        assert not serializer.is_valid()
        assert "order" in serializer.errors

