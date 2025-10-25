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

from .forms import CustomUserCreationForm, LoginForm

User = get_user_model()


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
    return render(request, "users/dashboard.html")
