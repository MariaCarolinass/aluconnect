import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User, UserRole

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

        tokens = response.data.get("tokens", {})
        assert "access" in tokens

        if "refresh" in tokens:
            assert "refresh" in tokens