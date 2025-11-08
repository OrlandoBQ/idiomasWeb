# study/admin.py
from django.contrib import admin
from .models import StudySession, Review

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "deck", "started_at", "finished_at", "duration_seconds")
    list_filter = ("deck", "started_at", "finished_at")
    search_fields = ("user__username", "deck__title")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "card", "score", "reviewed_at")
    list_filter = ("score", "reviewed_at")
    search_fields = ("card__front", "session__user__username")
