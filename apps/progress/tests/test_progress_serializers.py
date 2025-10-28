import pytest
from apps.users.models import User
from apps.users.constants import UserRole
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.progress.models import ProgressStatus
from apps.progress.serializers import ProgressSerializer


@pytest.mark.django_db
def test_student_progress_serializer_valid():
    student = User.objects.create_user(username="carol", email="carol@example.com", password="123", role=UserRole.STUDENT)
    course = Course.objects.create(title="Curso de Django")
    lesson = Lesson.objects.create(course=course, title="Aula 1", order=1)

    data = {
        "student": student.id,
        "lesson": lesson.id,
        "course": course.id,
        "status": ProgressStatus.COMPLETED
    }

    serializer = ProgressSerializer(data=data)
    assert serializer.is_valid()
    progress = serializer.save()
    assert progress.status == ProgressStatus.COMPLETED