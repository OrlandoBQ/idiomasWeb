from django.shortcuts import render
from django.http import HttpResponse

def study_home(request):
    return HttpResponse("Study Home - Elige una baraja para estudiar")

def start_study(request, deck_id):
    return HttpResponse(f"Comenzar estudio con la baraja {deck_id}")

def review_card(request, deck_id):
    return HttpResponse(f"Revisar tarjeta de la baraja {deck_id}")