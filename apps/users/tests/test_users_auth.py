import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole


@pytest.mark.django_db
class TestAuth:

    def setup_method(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')

    def test_register_user(self):
        data = {
            "email": "carol@example.com",
            "username": "carol",
            "password": "strongpass123",
            "role": UserRole.STUDENT
        }
        response = self.client.post(self.register_url, data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(email="carol@example.com").exists()

    def test_login_user(self):
        User.objects.create_user(
            email="carol@example.com",
            username="carol",
            password="strongpass123",
            role=UserRole.STUDENT
        )
        data = {"email": "carol@example.com", "password": "strongpass123"}
        response = self.client.post(self.login_url, data, format='json')
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_refresh_token(self):
        User.objects.create_user(
            email="carol@example.com",
            username="carol",
            password="strongpass123",
            role=UserRole.STUDENT
        )
        login_resp = self.client.post(self.login_url, {
            "email": "carol@example.com",
            "password": "strongpass123"
        }, format='json')
        refresh_token = login_resp.data["refresh"]
        response = self.client.post(self.refresh_url, {"refresh": refresh_token}, format='json')
        assert response.status_code == 200
        assert "access" in response.data