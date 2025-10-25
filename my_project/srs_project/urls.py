from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),
    

    # Rutas principales de cada app
    path('', views.landing_page, name='landing'),
    path('', include('users.urls')),       # Home, login, registro
    path('decks/', include('decks.urls')), # CRUD barajas/tarjetas
    path('study/', include('study.urls')), # Sesiones de estudio
    path('api/scheduler/', include('scheduler.urls')), # API repetición espaciada
    path('analytics/', include('analytics.urls')), # Progreso y métricas
    path('api/', include('api.urls')), # API RESTful
    path('help/', views.help_center, name='help_center'), # Centro de ayuda
    path('classes/', include('classes.urls')), # Gestión de clases y estudiantes

]
