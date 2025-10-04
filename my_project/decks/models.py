from django.db import models
from srs_project.choices import EstadoVisibility, EstadoTypes
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Deck(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    visibility = models.CharField(max_length=10, choices=EstadoVisibility.choices, default=EstadoVisibility.PRIVATE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.owner})"


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    card_type = models.CharField(max_length=20, choices=EstadoTypes.choices, default=EstadoTypes.BASIC)
    front = models.TextField()
    back = models.TextField()
    ease_factor = models.FloatField(default=2.5)
    interval = models.PositiveIntegerField(default=1)
    next_review = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Card {self.id} in {self.deck.title}"
