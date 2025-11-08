from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.class_list, name='class_list'),
    path('create/', views.create_lesson_class, name='class_create'),
    path('<int:pk>/', views.class_detail, name='class_detail'),
]
