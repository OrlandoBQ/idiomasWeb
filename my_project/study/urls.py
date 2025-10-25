from django.urls import path
from . import views

app_name = 'study'

urlpatterns = [
    path('start/<int:deck_id>/', views.start_study_session, name='start'),
]
