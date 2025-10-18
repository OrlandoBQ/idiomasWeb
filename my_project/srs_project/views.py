from django.shortcuts import render

def landing_page(request):
    return render(request, "landing.html")

def help_center(request):
    return render(request, 'help.html')