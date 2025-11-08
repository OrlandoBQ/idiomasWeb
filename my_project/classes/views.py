from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone

from .models import LessonClass, UserClassProgress
from .forms import LessonClassForm
from decks.models import Deck


def _is_teacher_or_admin(user):
    return user.is_staff or getattr(user, 'is_teacher', False)


@login_required
def class_list(request):
    """
    Muestra la lista de clases disponibles según el tipo de usuario.
    Además, calcula el estado del deck para el usuario:
    - not_started
    - in_progress
    - completed
    - review_due
    """

    qs = LessonClass.objects.select_related('deck', 'deck__owner').annotate(
        cards_count=Count('deck__cards')
    ).order_by('level', 'title')

    if _is_teacher_or_admin(request.user):
        classes_qs = qs  # Teachers/Admins ven todo
    else:
        public_q = Q(deck__visibility='public')
        own_q = Q(deck__owner=request.user)
        classes_qs = qs.filter(public_q | own_q).distinct()

    # Calculamos el estado del deck para cada clase (usando el método del modelo Deck)
    deck_statuses = {
        c.deck.id: c.deck.get_user_status(request.user)
        for c in classes_qs
    }

    today = timezone.localdate()

    return render(request, "classes/class_list.html", {
        "classes": classes_qs,
        "deck_statuses": deck_statuses,
        "today": today,
    })


@login_required
def class_detail(request, pk):
    """
    Muestra detalle de la clase.
    Bloquea acceso si deck es privado y el usuario no es owner ni teacher/admin.
    """
    lesson_class = get_object_or_404(
        LessonClass.objects.select_related('deck', 'deck__owner').prefetch_related('deck__cards'),
        pk=pk
    )

    deck = lesson_class.deck
    # Acceso: si el deck NO es público, solamente owner o teacher/admin pueden verlo
    if deck.visibility != 'public' and deck.owner != request.user and not _is_teacher_or_admin(request.user):
        messages.error(request, "No tienes permiso para ver esta clase.")
        return redirect('classes:class_list')

    progress, created = UserClassProgress.objects.get_or_create(user=request.user, lesson_class=lesson_class)

    if request.method == "POST":
        # Marcar como completada (solo para usuarios autenticados)
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, "Clase marcada como completada ✅")
        return redirect('classes:class_detail', pk=pk)

    return render(request, "classes/class_detail.html", {
        "lesson_class": lesson_class,
        "progress": progress
    })


@login_required
def create_lesson_class(request):
    """
    Solo docentes (o admins) pueden crear clases desde la UI.
    Limitamos el queryset de 'deck' para que los docentes solo puedan elegir sus propios decks.
    """
    if not _is_teacher_or_admin(request.user):
        messages.warning(request, "Solo los docentes pueden crear nuevas clases.")
        return redirect('classes:class_list')

    if request.method == "POST":
        form = LessonClassForm(request.POST)
        if not request.user.is_superuser:
            form.fields['deck'].queryset = Deck.objects.filter(owner=request.user)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            messages.success(request, "La clase se creó correctamente.")
            return redirect('classes:class_list')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = LessonClassForm()
        if not request.user.is_superuser:
            form.fields['deck'].queryset = Deck.objects.filter(owner=request.user)

    return render(request, "classes/lessonclass_form.html", {"form": form})
