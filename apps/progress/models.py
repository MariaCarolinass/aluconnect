from django.db import models
from apps.users.models import User
from apps.courses.models import Course
from apps.lessons.models import Lesson
from apps.progress.constants import ProgressStatus


class Progress(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'},
        related_name='progress_records',
        verbose_name='Estudante'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name='Curso'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name='Aula'
    )
    status = models.CharField(
        max_length=20,
        choices=ProgressStatus.CHOICES,
        default=ProgressStatus.STARTED,
        verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        unique_together = ('student', 'lesson')
        verbose_name = 'Progresso'
        verbose_name_plural = 'Progressos'
        ordering = ['-updated_at']

    def __str__(self):
        return f"Student: {self.student.get_full_name() or self.student.username} - Lesson: {self.lesson.title} - Status: ({self.status})"
