from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.constants import UserRole


class User(AbstractUser):
    username = models.CharField(max_length=20, verbose_name='Nome de usuário')
    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(
        max_length=20,
        choices=UserRole.CHOICES,
        default=UserRole.STUDENT,
        verbose_name='Papel do usuário'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['email']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"