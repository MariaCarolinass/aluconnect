import openai
from decouple import config
from celery import shared_task
from apps.certificates.models import Certificate
from apps.users.models import User
from apps.courses.models import Course
from apps.certificates.constants import CERTIFICATE_CODE_LENGTH
from config.utils import generate_unique_code

openai.api_key = config("OPENAI_API_KEY")

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def generate_certificate(self, student_id, course_id):
    """
    Task assíncrona que gera um certificado personalizado para um aluno que concluiu um curso.
    Utiliza OpenAI para gerar o texto e salva o certificado com um código único.
    """
    try:
        student = User.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        prompt = (
            f"Crie um texto de certificado de conclusão para um aluno chamado {student.username} "
            f"que terminou o curso '{course.title}'. O texto deve ser inspirador e ideal para compartilhar nas redes sociais."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que cria certificados de conclusão."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        personalized_text = response.choices[0].message["content"].strip()

        code = generate_unique_code(CERTIFICATE_CODE_LENGTH)

        Certificate.objects.get_or_create(
            student=student,
            course=course,
            code=code,
            defaults={"text": personalized_text}
        )

        return f"Certificado gerado para {student.email} no curso '{course.title}'."

    except (User.DoesNotExist, Course.DoesNotExist) as e:
        return f"Erro: {str(e)}"
    
    except Exception as e:
        self.retry(exc=e)