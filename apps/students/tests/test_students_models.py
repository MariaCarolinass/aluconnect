import pytest
from apps.users.models import User
from apps.users.constants import UserRole
from apps.students.models import Student


@pytest.mark.django_db
class TestStudentModel:

    def test_create_student(self):
        user = User.objects.create_user(
            email="carol@example.com",
            username="carol",
            password="test123",
            role=UserRole.STUDENT
        )
        student = Student.objects.create(
            user=user,
            is_active=True
        )
        assert student.user.email == "carol@example.com"
        assert student.is_active is True
        assert str(student) == "Estudante: carol"
