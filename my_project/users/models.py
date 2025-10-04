from django.contrib.auth.models import AbstractUser
from srs_project.choices import EstadoRoles
from django.db import models

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=20, choices=EstadoRoles.choices, default=EstadoRoles.STUDENT)
    language = models.CharField(max_length=20, default='es')
    streak_days = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
