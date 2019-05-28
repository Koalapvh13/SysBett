from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from appGastos.form import *

# Create your views here.
from appGastos.customAuthUser import CustomAuthUser


def do_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            auth = CustomAuthUser().authenticate(email=request.POST['email'], senha=request.POST['senha'])
            if auth is not None:
                login(request, auth)
                return HttpResponseRedirect('/despesa')
            else:
                return HttpResponseRedirect('/receita')
        return render(request, 'appGastos/signin.html', {'form': LoginForm()})
    return HttpResponseRedirect('/categoria')


def cadastro_usuario(request):
    if request.method == 'POST':
        salva = CustomUserCreationForm(request.POST)
        salva.is_valid()
        salva.save()
        return render(request, 'appGastos/cadCategoria.html', {'form': ReceitaForm(), 'title': "salvo"})
    else:
        dicio = {"form": CustomUserCreationForm(), "title": "Cadastrar Usuário"}
        return render(request, 'appGastos/signup.html', dicio)


def cadastro_categoria(request):
    dicio = {"form": CategoriaForm(), "title": "Cadastrar Categoria"}
    return render(request, 'appGastos/cadCategoria.html', dicio)


def cadastro_receita(request):
    dicio = {"form": ReceitaForm(), "title": "Cadastrar Receita"}
    return render(request, 'appGastos/cadCategoria.html', dicio)


def cadastro_despesa(request):
    dicio = {"form": DespesaForm(), "title": "Cadastrar Despesa"}
    return render(request, 'appGastos/cadCategoria.html', dicio)
