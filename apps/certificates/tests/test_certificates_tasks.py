import pytest
from unittest.mock import patch, MagicMock
from django.db import IntegrityError
from apps.certificates.tasks import generate_certificate
from apps.certificates.models import Certificate
from apps.users.models import User
from apps.courses.models import Course
from apps.certificates.constants import CERTIFICATE_CODE_LENGTH
from config.utils import generate_unique_code


@pytest.mark.django_db
class TestGenerateCertificateTask:

    def setup_method(self):
        self.student = User.objects.create_user(
            email="student@example.com",
            username="student",
            password="test123",
            role="STUDENT"
        )
        self.course = Course.objects.create(title="Curso de Teste")

    @patch("apps.certificates.tasks.client.chat.completions.create")
    @patch("apps.certificates.tasks.generate_unique_code")
    def test_generate_certificate_success(self, mock_code, mock_openai):
        mock_response = MagicMock()
        mock_response.choices[0].message.content.strip.return_value = "Certificado de teste"
        mock_openai.return_value = mock_response

        mock_code.return_value = "ABC123XYZ"

        result = generate_certificate(self.student.id, self.course.id)

        certificate = Certificate.objects.get(student=self.student, course=self.course)
        assert certificate.text == "Certificado de teste"
        assert certificate.code == "ABC123XYZ"
        assert result == f"Certificado gerado para {self.student.email} no curso '{self.course.title}'."

    @patch("apps.certificates.tasks.client.chat.completions.create")
    @patch("apps.certificates.tasks.generate_unique_code")
    def test_generate_certificate_already_exists(self, mock_code, mock_openai):
        Certificate.objects.create(
            student=self.student,
            course=self.course,
            code="EXIST123",
            text="Texto existente"
        )

        result = generate_certificate(self.student.id, self.course.id)
        assert result == f"Certificado já existente para {self.student.email} no curso '{self.course.title}'."

    def test_generate_certificate_user_not_found(self):
        result = generate_certificate(9999, self.course.id)
        assert "Erro: User matching query does not exist." in result

    def test_generate_certificate_course_not_found(self):
        result = generate_certificate(self.student.id, 9999)
        assert "Erro: Course matching query does not exist." in result

    @patch("apps.certificates.tasks.client.chat.completions.create")
    @patch("apps.certificates.tasks.generate_unique_code")
    def test_generate_certificate_integrity_error(self, mock_code, mock_openai):
        mock_response = MagicMock()
        mock_response.choices[0].message.content.strip.return_value = "Certificado de teste"
        mock_openai.return_value = mock_response
        mock_code.return_value = "ABC123XYZ"

        with patch("apps.certificates.tasks.Certificate.objects.create") as mock_create:
            mock_create.side_effect = IntegrityError()
            result = generate_certificate(self.student.id, self.course.id)

        assert f"Certificado já criado simultaneamente para {self.student.email}." in result
