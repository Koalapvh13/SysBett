from django import forms

from appGastos.admin import UserCreationForm
from appGastos.models import *


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


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.HiddenInput(attrs={'class': 'form-control'})
        }


class TransacaoReceitaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(tipo="Receita"), widget=forms.Select(attrs={'class': 'form-control'}),)
    class Meta:
        model = Transacao
        exclude = ['tipo', 'usuario']

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': "date"}),
        }


class TransacaoDespesaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(tipo="Despesa"), widget=forms.Select(attrs={'class': 'form-control'}),)

    class Meta:
        model = Transacao
        exclude = ['tipo', 'usuario']

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': "date"}),

        }


class RelatorioGeral(forms.Form):
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': "date"}))
    data_final = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': "date"}, format="%d/%m/%Y"), input_formats=("%d/%m/%Y",))