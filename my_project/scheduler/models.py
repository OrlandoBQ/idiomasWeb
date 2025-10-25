# Create your models here.
# Create your models here.
from django.db import models
from decks.models import Card
from django.conf import settings

User = settings.AUTH_USER_MODEL

class SchedulingData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    ease = models.FloatField(default=2.5)
    interval = models.PositiveIntegerField(default=1)
    repetitions = models.PositiveIntegerField(default=0)
    due_date = models.DateField(null=True, blank=True)
