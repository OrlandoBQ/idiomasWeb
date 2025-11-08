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

    # Crear nueva sesión
    session = StudySession.objects.create(
        user=request.user,
        deck=deck,
        mode=EstadoModes.CARDS,
        started_at=timezone.now(),
    )

    # Tomar la primera carta del deck
    first_card = Card.objects.filter(deck=deck).order_by('id').first()
    if not first_card:
        return render(request, "study/empty_deck.html", {"deck": deck})

    # Redirigir a review_card con la primera carta
    return redirect('study:review_card', session_id=session.id, card_id=first_card.id)



@login_required
def review_card(request, session_id, card_id=None):
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    
    # Todas las cartas del deck, ordenadas
    all_cards = list(Card.objects.filter(deck=session.deck).order_by('id'))
    if not all_cards:
        return render(request, "study/empty_deck.html", {"deck": session.deck})

    # Carta actual: si no hay card_id, tomar la primera
    if card_id:
        card = get_object_or_404(Card, id=card_id, deck=session.deck)
    else:
        card = all_cards[0]

    # Obtener o crear SchedulingData
    data, _ = SchedulingData.objects.get_or_create(user=request.user, card=card)

    if request.method == "POST":
        score = int(request.POST.get("score"))
        data.update_review(score)
        Review.objects.create(session=session, card=card, score=score)

        # Buscar siguiente carta
        current_index = all_cards.index(card)
        remaining = len(all_cards) - (current_index + 1)  # para mostrar progreso

        try:
            next_card = all_cards[current_index + 1]
            return redirect('study:review_card', session_id=session.id, card_id=next_card.id)
        except IndexError:
            # No quedan cartas → sesión completada
            session.finish()
            return render(request, 'study/session_complete.html', {'deck': session.deck})

    # Pasamos remaining para el template
    current_index = all_cards.index(card)
    remaining = len(all_cards) - (current_index + 1)

    return render(request, 'study/study_session.html', {
        'card': card,
        'session': session,
        'deck': session.deck,
        'remaining': remaining,
    })
