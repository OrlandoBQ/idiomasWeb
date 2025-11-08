from django.utils import timezone
from datetime import timedelta
from study.models import Review, UserClassProgress
from scheduler.models import SchedulingData
from django.db.models import Count

def reviews_today(user):
    today = timezone.now().date()
    return Review.objects.filter(session__user=user, reviewed_at__date=today).count()

def words_mastered(user):
    return SchedulingData.objects.filter(user=user, repetitions__gte=3).count()

def lessons_completed_today(user):
    today = timezone.now().date()
    return UserClassProgress.objects.filter(user=user, completed=True, completed_at__date=today).count()

def pending_cards_count(user):
    today = timezone.now().date()
    return SchedulingData.objects.filter(user=user, due_date__lte=today).count()
