import pytest
from apps.users.models import User
from apps.users.constants import UserRole

@pytest.mark.django_db
class TestUserModel:

    def test_create_student_user(self):
        user = User.objects.create_user(
            email="student@example.com",
            username="student",
            password="test123",
            role=UserRole.STUDENT
        )
        assert user.email == "student@example.com"
        assert user.role == UserRole.STUDENT
        assert user.is_active is True
        assert user.check_password("test123")

    def test_create_instructor_user(self):
        user = User.objects.create_user(
            email="instructor@example.com",
            username="instructor",
            password="test123",
            role=UserRole.INSTRUCTOR
        )
        assert user.role == UserRole.INSTRUCTOR

    def test_create_admin_user(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass"
        )
        assert user.is_superuser is True
        assert user.role == UserRole.STUDENT

    def test_str_representation(self):
        user = User.objects.create_user(
            email="carol@example.com",
            username="carol",
            password="test123"
        )
        assert str(user) == "carol (carol@example.com)"