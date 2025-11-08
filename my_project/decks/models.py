from django.db import models
from django.conf import settings
from core.choices import EstadoVisibility, EstadoTypes
from django.utils import timezone

AUTH_USER = settings.AUTH_USER_MODEL  # string reference, ok for migrations

class MasterClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Deck(MasterClass):
    owner = models.ForeignKey(AUTH_USER, on_delete=models.CASCADE, related_name='decks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    visibility = models.CharField(max_length=10, choices=EstadoVisibility.choices, default=EstadoVisibility.PRIVATE)
    deck_type = models.CharField(max_length=20, choices=EstadoTypes.choices, default=EstadoTypes.BASIC)
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Deck'
        verbose_name_plural = 'Decks'

    def __str__(self):
        return f"{self.title} ({self.owner})"

    def get_user_status(self, user):
        """
        Devuelve el estado del deck para un usuario específico:
        - not_started: nunca estudiado
        - in_progress: iniciado pero no completado
        - completed: completado una vez
        - review_due: hay tarjetas listas para repaso
        """
        if not user.is_authenticated:
            return 'not_started'

        # Importamos aquí adentro para evitar el circular import
        from classes.models import UserClassProgress
        from scheduler.models import SchedulingData

        today = timezone.localdate()

        # Buscar progreso de clases
        progress = UserClassProgress.objects.filter(user=user, lesson_class__deck=self).first()

        # Buscar tarjetas programadas para repaso
        cards_scheduled = SchedulingData.objects.filter(user=user, card__deck=self)

        if not progress and not cards_scheduled.exists():
            return 'not_started'

        if cards_scheduled.filter(due_date__lte=today).exists():
            return 'review_due'

        total_cards = self.cards.count()
        cards_studied = cards_scheduled.filter(repetitions__gte=1).count()

        if cards_studied >= total_cards:
            return 'completed'

        return 'in_progress'


class Card(MasterClass):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    card_type = models.CharField(max_length=20, choices=EstadoTypes.choices, default=EstadoTypes.BASIC)
    front = models.TextField()
    back = models.TextField()
    ease_factor = models.FloatField(default=2.5)
    interval = models.PositiveIntegerField(default=1)
    next_review = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['deck', 'id']

    def __str__(self):
        return f"Card {self.id} in {self.deck.title}"
