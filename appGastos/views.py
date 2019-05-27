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
                return HttpResponseRedirect('/restrito')
            else:
                return HttpResponseRedirect('/cadastro')
        return render(request, 'login_siscop/login2.html')
    return HttpResponseRedirect('/restrito')


def cadastro_usuario(request):
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
