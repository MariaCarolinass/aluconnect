import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole
from apps.students.models import Student


@pytest.mark.django_db
class TestStudentViews:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="carol@example.com",
            username="carol",
            password="test123",
            role=UserRole.STUDENT
        )
        self.client.force_authenticate(user=self.user)
        self.student = Student.objects.create(user=self.user, bio="Estudante dedicada")

    def test_list_students(self):
        url = reverse('student-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert any(s["email"] == "carol@example.com" for s in response.data)

    def test_detail_student(self):
        url = reverse('student-detail', args=[self.user.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["email"] == "carol@example.com"

    def test_update_student(self):
        url = reverse('student-update', args=[self.user.id])
        data = {"bio": "Nova bio atualizada", "is_active": False}
        response = self.client.put(url, data, content_type='application/json')
        assert response.status_code == 200
        self.student.refresh_from_db()
        assert self.student.bio == "Nova bio atualizada"
        assert self.student.is_active is False