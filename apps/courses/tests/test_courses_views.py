import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User
from apps.users.constants import UserRole
from apps.courses.models import Course


@pytest.mark.django_db
class TestCourseViews:

    def setup_method(self):
        self.client = APIClient()
        self.instructor = User.objects.create_user(
            email="prof@example.com",
            username="prof",
            password="test123",
            role=UserRole.INSTRUCTOR
        )
        self.student = User.objects.create_user(
            email="carol@example.com",
            username="carol",
            password="test123",
            role=UserRole.STUDENT
        )
        self.course = Course.objects.create(title="Curso de Python", description="Intro")
        self.course.instructors.add(self.instructor)

    def test_create_course(self):
        self.client.force_authenticate(user=self.instructor)
        data = {
            "title": "Curso de Django",
            "description": "Web com Python",
            "instructors": [self.instructor.id]
        }
        url = reverse('course-create')
        response = self.client.post(url, data, content_type='application/json')
        assert response.status_code == 201
        assert Course.objects.filter(title="Curso de Django").exists()

    def test_list_courses_public(self):
        url = reverse('course-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert any(c["title"] == "Curso de Python" for c in response.data)

    def test_detail_course(self):
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["title"] == "Curso de Python"

    def test_update_course(self):
        self.client.force_authenticate(user=self.instructor)
        data = {
            "title": "Curso Atualizado",
            "description": "Nova descrição",
            "instructors": [self.instructor.id]
        }
        url = reverse('course-update', args=[self.course.id])
        response = self.client.put(url, data, content_type='application/json')
        assert response.status_code == 200
        self.course.refresh_from_db()
        assert self.course.title == "Curso Atualizado"

    def test_enroll_student(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('course-enroll', args=[self.course.id])
        response = self.client.post(url)
        assert response.status_code == 200
        assert self.student in self.course.students.all()

    def test_list_student_courses(self):
        self.course.students.add(self.student)
        self.client.force_authenticate(user=self.student)
        url = reverse('student-courses', args=[self.student.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert any(c["title"] == "Curso de Python" for c in response.data)

    def test_list_instructor_courses(self):
        self.client.force_authenticate(user=self.instructor)
        url = reverse('instructor-courses', args=[self.instructor.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert any(c["title"] == "Curso de Python" for c in response.data)