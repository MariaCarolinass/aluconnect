import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole
from apps.courses.models import Course
from apps.lessons.models import Lesson
from rest_framework import status


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
        self.student = User.objects.create_user(
            username="alice",
            email="alice@student.com",
            password="123",
            role=UserRole.STUDENT
        )
        self.course = Course.objects.create(title="Curso de Django")
        self.course.instructors.add(self.instructor)

    def test_list_lessons(self):
        Lesson.objects.create(course=self.course, title="Aula 1", order=1)
        Lesson.objects.create(course=self.course, title="Aula 2", order=2)
        url = reverse('lesson-list', args=[self.course.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_create_lesson_as_instructor(self):
        self.client.force_authenticate(user=self.instructor)
        url = reverse('lesson-create', args=[self.course.id])
        data = {"title": "Nova Aula"}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Lesson.objects.filter(course=self.course, title="Nova Aula").exists()

    def test_create_lesson_as_student_forbidden(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('lesson-create', args=[self.course.id])
        data = {"title": "Nova Aula"}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_lesson_with_minimum_lessons_check(self):
        self.client.force_authenticate(user=self.instructor)
        lesson1 = Lesson.objects.create(course=self.course, title="Aula 1", order=1)
        lesson2 = Lesson.objects.create(course=self.course, title="Aula 2", order=2)
        url = reverse('lesson-delete', args=[self.course.id, lesson2.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Lesson.objects.filter(id=lesson2.id).exists()

    def test_delete_lesson_fails_if_minimum_not_met(self):
        self.client.force_authenticate(user=self.instructor)
        lesson1 = Lesson.objects.create(course=self.course, title="Aula 1", order=1)
        url = reverse('lesson-delete', args=[self.course.id, lesson1.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Lesson.objects.filter(id=lesson1.id).exists()
