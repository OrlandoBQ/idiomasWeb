from django import forms
from .models import LessonClass

class LessonClassForm(forms.ModelForm):
    class Meta:
        model = LessonClass
        fields = ['title', 'description', 'deck', 'level']
