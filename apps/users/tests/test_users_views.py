import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch


@pytest.mark.django_db
class TestUserViews:

    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="123",
            role=UserRole.ADMIN
        )
        self.student = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="123",
            role=UserRole.STUDENT
        )

    def test_login_returns_tokens(self):
        url = reverse('login')
        data = {"email": self.student.email, "password": "123"}
        response = self.client.post(url, data, format='json')
        assert response.status_code == 200
        assert response.data["user"]["email"] == self.student.email
        assert "access" in response.data["tokens"]

    def test_logout_success(self):
        self.client.force_authenticate(user=self.student)
        refresh = RefreshToken.for_user(self.student)
        url = reverse('logout')
        data = {"refresh": str(refresh)}
        response = self.client.post(url, data, format='json')
        assert response.status_code == 200
        assert "Logout realizado com sucesso" in response.data["detail"]

    def test_logout_invalid_token(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('logout')
        data = {"refresh": "invalidtoken"}
        response = self.client.post(url, data, format='json')
        assert response.status_code == 400
        assert "error" in response.data
