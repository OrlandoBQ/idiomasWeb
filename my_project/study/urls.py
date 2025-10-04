from django.urls import path
from . import views

app_name = 'study'

urlpatterns = [
    path('', views.study_home, name='home'),
    path('<int:deck_id>/start/', views.start_study, name='start'),
    path('<int:deck_id>/review/', views.review_card, name='review'),
]
