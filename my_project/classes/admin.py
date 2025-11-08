from django.contrib import admin
from .models import LessonClass, UserClassProgress

@admin.register(LessonClass)
class LessonClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'deck', 'level', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('title', 'description')

@admin.register(UserClassProgress)
class UserClassProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson_class', 'completed', 'completed_at')
    list_filter = ('completed',)
    search_fields = ('user__username', 'lesson_class__title')
