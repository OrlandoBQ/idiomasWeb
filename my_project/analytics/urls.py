from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard, name='dashboard'),
    path('decks/<int:deck_id>/', views.deck_stats, name='deck_stats'),
]
