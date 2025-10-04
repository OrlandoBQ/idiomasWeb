from django.db import models
from srs_project.choices import EstadoModes, EstadoQuality
from django.conf import settings
from decks.models import Deck, Card

User = settings.AUTH_USER_MODEL

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='sessions')
    mode = models.CharField(max_length=20, choices=EstadoModes.choices, default=EstadoModes.CARDS)
    started_at = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Session by {self.user} on {self.deck.title}"


class Review(models.Model):
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='reviews')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='reviews')
    quality = models.IntegerField(choices=EstadoQuality.choices)
    response_time_ms = models.IntegerField(default=0)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.card.id} ({self.quality})"
