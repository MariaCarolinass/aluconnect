from apps.lessons.models import Lesson
import logging

logger = logging.getLogger(__name__)

def course_has_minimum_lessons(course, minimum=1, log=False):
    """
    Verifica se o curso possui pelo menos 'minimum' aulas.
    Retorna True se o número de aulas for suficiente, False caso contrário.
    """
    count = Lesson.objects.filter(course=course).count()
    if log:
        logger.info(f"Curso '{course.title}' possui {count} aulas (mínimo exigido: {minimum})")
    return count >= minimum
