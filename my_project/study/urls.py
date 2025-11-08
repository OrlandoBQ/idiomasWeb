from django.urls import path
from . import views

app_name = 'study'

urlpatterns = [
    path('start/<int:deck_id>/', views.start_study_session, name='start'),
    path('review/<int:session_id>/<int:card_id>/', views.review_card, name='review_card'),
]
