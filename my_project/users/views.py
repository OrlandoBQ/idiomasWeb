from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404
from decks.models import Deck
from .forms import CustomUserCreationForm, LoginForm
from study.models import StudySession, Review
from classes.models import UserClassProgress
from scheduler.models import SchedulingData
from django.utils import timezone

User = get_user_model()

def user_profile(request, username):
    """
    Muestra el perfil público de un usuario:
      - own_decks: todos los decks del usuario perfilado
      - public_decks_by_others: decks públicos creados por otros usuarios
    Se usa username__iexact para evitar problemas con mayúsculas/minúsculas.
    """
    profile_user = get_object_or_404(User, username__iexact=username)

    own_decks = Deck.objects.filter(owner=profile_user).select_related('owner').order_by('title')

    public_decks_by_others = (
        Deck.objects
        .filter(visibility='public')
        .exclude(owner=profile_user)
        .select_related('owner')
        .order_by('title')
    )

    context = {
        "profile_user": profile_user,
        "own_decks": own_decks,
        "public_decks_by_others": public_decks_by_others,
    }
    return render(request, "users/profile.html", context)


def home(request):
    return render(request, "users/home.html")


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 👈 cuenta inactiva hasta verificar
            user.save()

            send_verification_email(request, user)
            messages.info(request, "Hemos enviado un correo de verificación a tu dirección. Verifica tu cuenta para continuar.")
            return redirect('users:email_sent')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = f"http://{domain}/activate/{uid}/{token}/"

    subject = "Activa tu cuenta en LinguaLeap"
    message = render_to_string("users/email_verification.html", {
        "user": user,
        "activation_link": link,
    })

    send_mail(
        subject,
        message,
        "no-reply@lingualeap.com",
        [user.email],
        fail_silently=False,
    )


def email_sent_view(request):
    return render(request, "users/email_sent.html")


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tu cuenta ha sido activada. Ya puedes iniciar sesión.")
        return redirect('users:login')
    else:
        messages.error(request, "El enlace de activación no es válido o ha expirado.")
        return redirect('users:signup')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                if not user.is_active:
                    messages.warning(request, "Tu cuenta aún no ha sido activada. Revisa tu correo.")
                    return redirect('users:email_sent')
                login(request, user)
                messages.success(request, f"Bienvenido/a {user.username}!")
                return redirect('users:dashboard')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('users:home')

@login_required
def dashboard_view(request):
    user = request.user

    # Ajustar la fecha local para comparaciones
    today = timezone.localtime(timezone.now()).date()

    # 1) Revisiones hechas hoy
    reviews_today = Review.objects.filter(
        session__user=user,
        reviewed_at__date=today
    ).count()

    # 2) Palabras dominadas (criterio: repetitions >= 3)
    mastered = SchedulingData.objects.filter(user=user, repetitions__gte=3).count()

    # 3) Racha guardada en el user (si tienes user.streak_days)
    streak = getattr(user, "streak_days", 0)

    # 4) Progreso objetivos: ejemplo "Completar 5 lecciones diarias"
    lessons_goal = 5
    lessons_completed_today = UserClassProgress.objects.filter(
        user=user,
        completed=True,
        completed_at__date=today
    ).count()
    progress_pct = min(100, int(lessons_completed_today / lessons_goal * 100)) if lessons_goal else 0

    # 5) Tarjetas pendientes (due hoy)
    pending_cards = SchedulingData.objects.filter(user=user, due_date__lte=today).count()

    context = {
        "reviews_today": reviews_today,
        "mastered": mastered,
        "streak": streak,
        "lessons_goal": lessons_goal,
        "lessons_completed_today": lessons_completed_today,
        "progress_pct": progress_pct,
        "pending_cards": pending_cards,
    }
    return render(request, "users/dashboard.html", context)


@login_required
def progress(request):
    user = request.user
    today = timezone.localtime(timezone.now()).date()

    # Palabras dominadas (repetidas >= 3 veces)
    mastered = SchedulingData.objects.filter(user=user, repetitions__gte=3).count()

    # Revisiones hoy
    reviews_today = Review.objects.filter(
        session__user=user,
        reviewed_at__date=today
    ).count()

    # Tarjetas pendientes
    pending_cards = SchedulingData.objects.filter(user=user, due_date__lte=today).count()

    context = {
        'mastered': mastered,
        'reviews_today': reviews_today,
        'pending_cards': pending_cards,
    }
    return render(request, 'users/progress.html', context)