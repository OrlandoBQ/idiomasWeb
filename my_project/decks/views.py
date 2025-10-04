from django.shortcuts import render
from django.http import HttpResponse

def deck_list(request):
    return HttpResponse("Lista de barajas")

def deck_create(request):
    return HttpResponse("Crear baraja")

def deck_detail(request, deck_id):
    return HttpResponse(f"Detalle de baraja {deck_id}")

def deck_edit(request, deck_id):
    return HttpResponse(f"Editar baraja {deck_id}")
