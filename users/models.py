from django.contrib.auth.models import AbstractUser
from django.db import models

from service.models import NULLABLE


class User(AbstractUser):
    """Модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name='email')

    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)  # номер телефона
    name = models.CharField(max_length=100, verbose_name='Имя')  # Имя пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [('can_view_users', 'can_view_users'),
                       ('can_block_users', 'can_block_users')]

