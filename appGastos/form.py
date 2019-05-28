from django import forms

from appGastos.admin import UserCreationForm
from appGastos.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['nome', 'email']


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'email'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'senha'}))


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = '__all__'

        widgets = {
            'tipo': forms.HiddenInput(attrs={'value': 1})
        }


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = '__all__'

        widgets = {
            'tipo': forms.HiddenInput(attrs={'value': 0})
        }
