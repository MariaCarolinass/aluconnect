from django.db import models
from apps.users.models import User
from apps.courses.models import Course


class Certificate(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'},
        related_name='certificates',
        verbose_name='Estudante'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name='Curso'
    )
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name='Emitido em')
    code = models.CharField(max_length=20, unique=True, verbose_name='Código do certificado')

    class Meta:
        unique_together = ('student', 'course')
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['-issued_at']

    def __str__(self):
        return f"Certificado {self.code} - {self.student.get_full_name() or self.student.username} - {self.course.title}"
