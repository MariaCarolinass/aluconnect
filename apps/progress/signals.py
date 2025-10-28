from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.progress.models import Progress, ProgressStatus
from apps.progress.services.progressService import has_completed_course
from apps.certificates.tasks import generate_certificate

@receiver(post_save, sender=Progress)
def check_course_completion(sender, instance, created, **kwargs):
    if not created or instance.status != ProgressStatus.COMPLETED:
        return

    student = instance.student
    course = instance.lesson.course

    if has_completed_course(student, course):
        generate_certificate.delay(student.id, course.id)
