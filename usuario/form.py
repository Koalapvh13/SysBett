from django import forms

from usuario.admin import UserCreationForm
from usuario.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['nome', 'email']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo...'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder': 'E-mail...'})
        }


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder': 'E-mail...'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'senha', 'class': 'form-control', 'placeholder': '******'}))

