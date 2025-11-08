# study/models.py
from django.db import models
from django.conf import settings
from decks.models import Deck, Card
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='study_sessions')
    mode = models.CharField(max_length=30, default='cards')  # o usa tu EstadoModes
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)

    def finish(self):
        if not self.finished_at:
            self.finished_at = timezone.now()
            # opcional: calcular duración si started_at existe
            try:
                self.duration_seconds = int((self.finished_at - self.started_at).total_seconds())
            except Exception:
                self.duration_seconds = 0
            self.save()

    def __str__(self):
        return f"Session {self.id} by {self.user} on {self.deck.title}"


class Review(models.Model):
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='reviews')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()  # 0-5
    response_time_ms = models.PositiveIntegerField(default=0)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} - {self.card.front[:20]} ({self.score})"

