from apps.lessons.models import Lesson
from apps.progress.models import Progress, ProgressStatus

def has_completed_course(student, course):
    total_lessons = course.lessons.count()

    if total_lessons == 0:
        return False

    completed_lessons = Progress.objects.filter(
        student=student,
        course=course,
        status=ProgressStatus.COMPLETED
    ).values_list('lesson_id', flat=True).distinct().count()

    return completed_lessons == total_lessons