from django import forms

from appGastos.admin import UserCreationForm
from appGastos.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['nome', 'email']


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder': 'E-mail...'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'senha', 'class': 'form-control', 'placeholder': '******'}))


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.HiddenInput(attrs={'class': 'form-control'})
        }


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        exclude = ['tipo', 'usuario']

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),

        }


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        exclude = ['tipo', 'usuario']

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),

        }


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = '__all__'

        widgets = {
            'tipo': forms.HiddenInput(attrs={'value': 0})
        }
