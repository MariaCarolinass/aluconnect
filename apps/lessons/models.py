from django.db import models
from apps.courses.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Curso'
    )
    title = models.CharField(max_length=100, verbose_name='Título da aula')
    content = models.TextField(blank=True, verbose_name='Conteúdo')
    order = models.PositiveIntegerField(default=1, verbose_name='Ordem')
    duration = models.DurationField(null=True, blank=True, verbose_name='Duração estimada')
    video_url = models.URLField(blank=True, verbose_name='Link do vídeo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['order']
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        constraints = [
            models.UniqueConstraint(fields=['course', 'order'], name='unique_lesson_order_per_course')
        ]

    def __str__(self):
        return f"Aula: {self.title}"
