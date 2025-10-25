from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decks.models import Deck, Card
from .models import StudySession, Review
from scheduler.models import SchedulingData
from core.choices import EstadoModes

@login_required
def start_study_session(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    
    # Crear una nueva sesión
    session = StudySession.objects.create(
        user=request.user,
        deck=deck,
        mode=EstadoModes.CARDS,
        started_at=timezone.now(),
    )
    
    # Opcional: obtener tarjetas pendientes (por algoritmo SM-2)
    due_cards = SchedulingData.objects.filter(
        user=request.user,
        card__deck=deck,
        due_date__lte=timezone.now().date()
    ).select_related('card')
    
    # Si no hay scheduling, muestra todas las cartas del deck
    if not due_cards.exists():
        due_cards = Card.objects.filter(deck=deck)
    
    # Mostrar la primera carta al usuario
    first_card = due_cards.first()
    
    if not first_card:
        return render(request, 'study/empty_deck.html', {'deck': deck})
    
    return render(request, 'study/study_session.html', {
        'deck': deck,
        'session': session,
        'card': first_card,
    })
