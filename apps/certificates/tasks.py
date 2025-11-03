from openai import OpenAI
from decouple import config
from celery import shared_task
from django.db import IntegrityError
from apps.certificates.models import Certificate
from apps.users.models import User
from apps.courses.models import Course
from apps.certificates.constants import CERTIFICATE_CODE_LENGTH
from config.utils import generate_unique_code
from datetime import datetime

client = OpenAI(
    api_key=config("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def generate_certificate(self, student_id, course_id):
    """
    Gera um certificado personalizado para o aluno usando a API gratuita do OpenRouter.
    Garante que não haja duplicação (safe and idempotent).
    """
    try:
        student = User.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        existing = Certificate.objects.filter(student=student, course=course).first()
        if existing:
            return f"Certificado já existente para {student.email} no curso '{course.title}'."

        current_date = datetime.now().strftime("%d/%m/%Y")
        
        prompt = (
            f"Crie um texto breve e inspirador de certificado de conclusão para o aluno {student.username} "
            f"que finalizou o curso '{course.title}' na data {current_date} pela instituição AluConnect."
        )

        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "Você é um assistente que escreve certificados de conclusão de curso."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        personalized_text = response.choices[0].message.content.strip()
        code = generate_unique_code(CERTIFICATE_CODE_LENGTH)

        Certificate.objects.create(
            student=student,
            course=course,
            code=code,
            text=personalized_text
        )

        return f"Certificado gerado para {student.email} no curso '{course.title}'."
    except (User.DoesNotExist, Course.DoesNotExist) as e:
        return f"Erro: {str(e)}"
    except IntegrityError:
        return f"Certificado já criado simultaneamente para {student.email}."
    except Exception as e:
        if "IntegrityError" in str(type(e)):
            return f"Erro de integridade detectado (não será feito retry)."
        self.retry(exc=e)