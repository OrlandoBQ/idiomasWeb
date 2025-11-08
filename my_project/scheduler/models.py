from django.db import models
from django.conf import settings
from decks.models import Card
from datetime import date, timedelta

User = settings.AUTH_USER_MODEL

class SchedulingData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    ease_factor = models.FloatField(default=2.5)  # Nivel de facilidad (SM-2)
    interval = models.PositiveIntegerField(default=1)  # Días entre repasos
    repetitions = models.PositiveIntegerField(default=0)  # Cuántas veces se ha visto
    due_date = models.DateField(default=date.today)  # Próxima fecha de repaso

    class Meta:
        unique_together = ('user', 'card')

    def __str__(self):
        return f"{self.user} - {self.card.front} (Repite en {self.due_date})"

    # Método útil para actualizar según la calidad de la respuesta (0–5)
    def update_review(self, quality: int):
        """
        Actualiza ease_factor, interval y due_date usando el algoritmo SM-2 básico.
        quality = [0-5], donde 5 significa respuesta perfecta.
        """
        if quality < 3:
            self.repetitions = 0
            self.interval = 1
        else:
            self.repetitions += 1
            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.ease_factor)

            # Ajustar el ease_factor
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Nueva fecha de repaso
        self.due_date = date.today() + timedelta(days=self.interval)
        self.save()
