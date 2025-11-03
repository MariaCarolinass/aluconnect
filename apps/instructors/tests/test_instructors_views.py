import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole
from apps.instructors.models import Instructor


@pytest.mark.django_db
class TestInstructorViews:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="carol@example.com",
            username="carol",
            password="test123",
            role=UserRole.STUDENT
        )
        self.client.force_authenticate(user=self.user)

    def test_list_instructors(self):
        instructor_user = User.objects.create_user(
            email="prof@example.com",
            username="prof",
            password="test123",
            role=UserRole.INSTRUCTOR
        )
        Instructor.objects.create(user=instructor_user, bio="Especialista em IA")
        url = reverse('instructor-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert any(i["email"] == "prof@example.com" for i in response.data)

    def test_detail_instructor(self):
        self.user.role = UserRole.INSTRUCTOR
        self.user.save()
        profile = Instructor.objects.create(user=self.user)
        url = reverse('instructor-detail', args=[profile.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["email"] == "carol@example.com"

    def test_update_instructor_profile(self):
        self.user.role = UserRole.INSTRUCTOR
        self.user.save()
        profile = Instructor.objects.create(user=self.user)
        data = {"bio": "Nova bio atualizada", "title": "Engenheira de Software"}
        url = reverse('instructor-update', args=[profile.id])
        response = self.client.put(url, data, content_type='application/json')
        assert response.status_code == 200
        profile.refresh_from_db()
        assert profile.bio == "Nova bio atualizada"
        assert profile.title == "Engenheira de Software"