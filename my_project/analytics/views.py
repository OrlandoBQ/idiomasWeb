from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def analytics_dashboard(request):
    return HttpResponse("Analytics Dashboard - Progreso y métricas de estudio")

def deck_stats(request):
    return HttpResponse("Progreso del usuario")