from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    language = forms.ChoiceField(
        choices=[
            ('en', 'Inglés'),
            ('fr', 'Francés'),
            ('de', 'Alemán'),
            ('it', 'Italiano'),
            ('pt', 'Portugués'),
        ],
        required=False,
        label="Idioma"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'language', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-input w-full px-4 py-3 border-2 border-gray-200 '
                         'dark:border-gray-700 bg-transparent rounded-lg '
                         'text-gray-900 dark:text-white focus:border-primary focus:ring-primary',
            })

        # Personaliza placeholders individualmente
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['email'].widget.attrs['placeholder'] = 'Correo electrónico'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'
        self.fields['language'].widget.attrs['class'] += ' form-select'
        self.fields['avatar'].widget.attrs['class'] += ' file-input'


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'form-input w-full px-4 py-3 border-2 border-gray-200 '
                     'dark:border-gray-700 bg-transparent rounded-lg '
                     'text-gray-900 dark:text-white focus:border-primary focus:ring-primary'
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-input w-full px-4 py-3 border-2 border-gray-200 '
                     'dark:border-gray-700 bg-transparent rounded-lg '
                     'text-gray-900 dark:text-white focus:border-primary focus:ring-primary'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        cleaned_data['user'] = user
        return cleaned_data
