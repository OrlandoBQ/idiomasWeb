from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Home - Bienvenido a la app de idiomas")

def signup_view(request):
    return HttpResponse("Registro de usuario")

def login_view(request):
    return HttpResponse("Login de usuario")

def logout_view(request):
    return HttpResponse("Logout de usuario")

def dashboard_view(request):
    return HttpResponse("Dashboard del usuario")

