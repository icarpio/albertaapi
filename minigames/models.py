from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import secrets

class User(AbstractUser):
    score = models.IntegerField(default=0)   
    coins = models.IntegerField(default=0)

    # Evitar conflictos de relaciones M2M con nombres únicos
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class PlayerGameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    game = models.CharField(max_length=100)  # Se pasa como string
    score = models.IntegerField(default=0)
    played_at = models.DateTimeField(auto_now_add=True)