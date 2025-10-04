from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def next_review(request):
    return HttpResponse("Próxima revisión programada")