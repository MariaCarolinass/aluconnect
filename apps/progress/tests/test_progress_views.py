import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.progress.models import Progress, ProgressStatus


@pytest.mark.django_db
class TestProgressViews:

    def setup_method(self):
        self.client = APIClient()
        self.student = User.objects.create_user(
            email="carol@student.com",
            username="carol",
            password="test123",
            role=UserRole.STUDENT
        )
        self.client.force_authenticate(user=self.student)
        self.course = Course.objects.create(title="Curso de Python")
        self.lesson1 = Lesson.objects.create(course=self.course, title="Aula 1")
        self.lesson2 = Lesson.objects.create(course=self.course, title="Aula 2")

    def test_register_progress_sets_status_completed(self):
        url = reverse('register-progress', args=[self.course.id, self.lesson1.id])
        response = self.client.post(url)
        assert response.status_code == 201
        progress = Progress.objects.get(student=self.student, lesson=self.lesson1)
        assert progress.status == ProgressStatus.COMPLETED

    def test_block_progress_if_course_completed(self):
        Progress.objects.create(student=self.student, course=self.course, lesson=self.lesson1, status=ProgressStatus.COMPLETED)
        Progress.objects.create(student=self.student, course=self.course, lesson=self.lesson2, status=ProgressStatus.COMPLETED)
        url = reverse('register-progress', args=[self.course.id, self.lesson1.id])
        response = self.client.post(url)
        assert response.status_code == 403
        assert response.data["detail"] == "Curso já concluído. Progresso não pode ser alterado."

    def test_list_all_progress_with_status(self):
        Progress.objects.create(student=self.student, course=self.course, lesson=self.lesson1, status=ProgressStatus.COMPLETED)
        url = reverse('student-progress', args=[self.student.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["status"] == ProgressStatus.COMPLETED

    def test_list_course_progress_with_status(self):
        Progress.objects.create(student=self.student, course=self.course, lesson=self.lesson1, status=ProgressStatus.COMPLETED)
        url = reverse('student-course-progress', args=[self.student.id, self.course.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["lesson"] == self.lesson1.id
        assert response.data[0]["status"] == ProgressStatus.COMPLETED
