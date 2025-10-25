from django.db import models
from django.conf import settings
from decks.models import Deck
from core.choices import EstadoNivel

User = settings.AUTH_USER_MODEL

class LessonClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='lesson_classes')
    level = models.CharField(max_length=50, choices=EstadoNivel.choices, default=EstadoNivel.BEGINNER)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserClassProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_class = models.ForeignKey(LessonClass, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson_class')

    def __str__(self):
        return f"{self.user} - {self.lesson_class} ({'✔️' if self.completed else '❌'})"
