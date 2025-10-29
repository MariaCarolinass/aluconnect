from django.db import models
from apps.users.models import User


class Instructor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_profile',
        verbose_name='Usuário'
    )
    title = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ex: Engenheiro de Software, Especialista em IA",
        verbose_name='Título profissional'
    )
    bio = models.TextField(blank=True, verbose_name='Biografia')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Instrutor'
        verbose_name_plural = 'Instrutores'
        ordering = ['user__username']

    def deactivate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Instrutor: {self.user.username}"
    