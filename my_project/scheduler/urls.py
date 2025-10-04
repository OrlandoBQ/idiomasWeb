from django.urls import path
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('next-review/', views.next_review, name='next_review'),
]
