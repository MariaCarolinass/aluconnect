from django.db import models
from apps.users.models import User
from django.utils import timezone
from datetime import timedelta


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Usuário'
    )
    bio = models.TextField(blank=True, verbose_name='Biografia')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'
        ordering = ['user__username']

    def is_blocked(self):
        """
        Retorna True se o aluno estiver bloqueado temporariamente
        """
        if self.blocked_until and self.blocked_until > timezone.now():
            return True
        return False

    def block_for(self, hours=24):
        """
        Bloqueia o aluno temporariamente
        """
        self.blocked_until = timezone.now() + timedelta(hours=hours)
        self.save()

    def __str__(self):
        return f"Estudante: {self.user.username}"
