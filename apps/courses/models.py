from django.db import models
from apps.users.models import User


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descrição')
    instructors = models.ManyToManyField(
        User,
        related_name='courses_taught',
        limit_choices_to={'role': 'INSTRUCTOR'},
        verbose_name='Instrutores'
    )
    students = models.ManyToManyField(
        User,
        related_name='courses_enrolled',
        blank=True,
        limit_choices_to={'role': 'STUDENT'},
        verbose_name='Alunos'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['title']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return f"Curso: {self.title}"
