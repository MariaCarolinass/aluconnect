import pytest
from apps.users.models import User
from apps.users.constants import UserRole
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.progress.models import Progress, ProgressStatus


@pytest.mark.django_db
class TestProgressModel:

    def setup_method(self):
        self.student = User.objects.create_user(username="carol", email="carol@example.com", password="123", role=UserRole.STUDENT)
        self.course = Course.objects.create(title="Curso de Django")
        self.lesson = Lesson.objects.create(course=self.course, title="Aula 1", order=1)

    def test_create_progress(self):
        progress = Progress.objects.create(student=self.student, course=self.course, lesson=self.lesson, status=ProgressStatus.COMPLETED)
        assert progress.student == self.student
        assert progress.lesson == self.lesson
        assert progress.status == ProgressStatus.COMPLETED

    def test_progress_is_unique_per_student_lesson(self):
        Progress.objects.create(student=self.student, course=self.course, lesson=self.lesson, status=ProgressStatus.COMPLETED)
        with pytest.raises(Exception):
            Progress.objects.create(student=self.student, course=self.course, lesson=self.lesson, status=ProgressStatus.COMPLETED)