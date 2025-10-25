from django.contrib.auth.models import AbstractUser
from core.choices import EstadoRoles, EstadoIdiomas
from django.db import models

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=20, choices=EstadoRoles.choices, default=EstadoRoles.STUDENT)
    language = models.CharField(max_length=20, choices=EstadoIdiomas.choices, default=EstadoIdiomas.EN)
    streak_days = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
