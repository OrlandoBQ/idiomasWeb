from django.urls import path
from . import views

app_name = 'decks'

urlpatterns = [
    path('', views.deck_list, name='list'),
    path('create/', views.deck_create, name='create'),
    path('<int:deck_id>/', views.deck_detail, name='detail'),
    path('<int:deck_id>/edit/', views.deck_edit, name='edit'),
]
