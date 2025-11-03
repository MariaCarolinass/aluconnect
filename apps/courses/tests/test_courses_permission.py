import pytest
from unittest.mock import MagicMock
from apps.users.constants import UserRole
from apps.courses.permissions import IsInstructor


@pytest.mark.django_db
class TestIsInstructorPermission:

    def setup_method(self):
        self.permission = IsInstructor()

    def test_instructor_has_permission(self):
        user = MagicMock()
        user.is_authenticated = True
        user.role = UserRole.INSTRUCTOR

        request = MagicMock()
        request.user = user

        assert self.permission.has_permission(request, view=None) is True

    def test_student_does_not_have_permission(self):
        user = MagicMock()
        user.is_authenticated = True
        user.role = UserRole.STUDENT

        request = MagicMock()
        request.user = user

        assert self.permission.has_permission(request, view=None) is False

    def test_anonymous_user_does_not_have_permission(self):
        user = MagicMock()
        user.is_authenticated = False
        user.role = None

        request = MagicMock()
        request.user = user

        assert self.permission.has_permission(request, view=None) is False

    def test_no_user_attached_to_request(self):
        request = MagicMock()
        request.user = None

        assert self.permission.has_permission(request, view=None) is False
