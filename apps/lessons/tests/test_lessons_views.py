import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole
from apps.courses.models import Course
from apps.lessons.models import Lesson


@pytest.mark.django_db
class TestLessonViews:

    def setup_method(self):
        self.client = APIClient()
        self.instructor = User.objects.create_user(
            username="carol",
            email="carol@example.com",
            password="123",
            role=UserRole.INSTRUCTOR
        )
        self.client.force_authenticate(user=self.instructor)
        self.course = Course.objects.create(title="Curso de Django")

    def test_create_lesson(self):
        url = reverse('lesson-create', args=[self.course.id])
        data = {"title": "Aula 1", "order": 1}
        response = self.client.post(url, data, content_type='application/json')
        assert response.status_code == 201
        assert response.data["title"] == "Aula 1"

    def test_list_lessons(self):
        Lesson.objects.create(course=self.course, title="Aula 1", order=1)
        Lesson.objects.create(course=self.course, title="Aula 2", order=2)
        url = reverse('lesson-list', args=[self.course.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(course=self.course, title="Aula 1", order=1)
        url = reverse('lesson-delete', args=[self.course.id, lesson.id])
        response = self.client.delete(url)
        assert response.status_code == 204
