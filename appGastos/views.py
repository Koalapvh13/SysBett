from django.contrib.auth import login, logout
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
    return HttpResponseRedirect('/admin')


def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login')


def index(request):
    dicio = {"transacao": Transacao.objects.filter(usuario=request.user).order_by('-data'),
             "lenT": len(Transacao.objects.filter(usuario=request.user).order_by('data')),
             "title": "Receitas"}
    return render(request, 'appGastos/dashboard.html', dicio)


def cadastro_usuario(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            salva = CustomUserCreationForm(request.POST)
            salva.is_valid()
            salva.save()
            return render(request, 'appGastos/cadCategoria.html', {'form': TransacaoForm(), 'title': "salvo"})
        else:
            dicio = {"form": CustomUserCreationForm(), "title": "Cadastrar Usuário"}
            return render(request, 'appGastos/signup.html', dicio)

@login_required
def cadastro_categoria(request):
    dicio = {"form": CategoriaForm(), "title": "Cadastrar Categoria", 'urli': 'categoria'}
    return render(request, 'appGastos/cadCategoria.html', dicio)


@login_required
def cadastro_receita(request):
    if request.user.is_authenticated and request.method == 'POST':
        salva = TransacaoForm(request.POST)
        if salva.is_valid():
            receita = salva.save(commit=False)
            receita.usuario = request.user
            receita.tipo = 0
            receita.save()
            return HttpResponseRedirect('/categoria')
    dicio = {"form": TransacaoForm(), "title": "Cadastrar Receita", 'urli': 'receita'}
    return render(request, 'appGastos/cadTransacao.html', dicio)


@login_required
def cadastro_despesa(request):
    if request.user.is_authenticated and request.method == 'POST':
        salva = TransacaoForm(request.POST)
        if salva.is_valid():  # TODO - FAZER ESSA DESGRAÇA SALVAR
            despesa = salva.save(commit=False)
            despesa.usuario = request.user
            despesa.tipo = 1
            despesa.save()
            return HttpResponseRedirect('/receita')
    dicio = {"form": TransacaoForm(), "title": "Cadastrar Despesa", 'urli': 'despesa'}
    return render(request, 'appGastos/cadTransacao.html', dicio)


@login_required
def listagem_despesa(request):
    dicio = {"transacao": Transacao.objects.filter(tipo="1", usuario=request.user).order_by('data'), "lenT": len(Transacao.objects.filter(tipo="1", usuario=request.user).order_by('data')), "title": "Despesas"}
    return render(request, 'appGastos/listagem.html', dicio)


@login_required
def listagem_receita(request):
    dicio = {"transacao": Transacao.objects.filter(tipo="0", usuario=request.user).order_by('data'),
             "lenT": len(Transacao.objects.filter(tipo="0", usuario=request.user).order_by('data')),
             "title": "Receitas"}
    return render(request, 'appGastos/listagem.html', dicio)


@login_required
def descricao_conta(request, idit):
    dicio = {"transacao": Transacao.objects.filter(pk=idit, usuario=request.user),
             "title": "Beirute"}
    return render(request, 'appGastos/item.html', dicio)


def api_transacoes(request, transacao):
    if request.user.is_authenticated:
        lbls = []
        values = []
        data = {}
        if transacao == 'despesa':
            tipo_transacao = 1
        elif transacao == 'receita':
            tipo_transacao = 0
        else:
            data = {
                "labels": "NdA",
                'values': 0
            }
            return JsonResponse(data)

        for i in Transacao.objects.filter(tipo=tipo_transacao, usuario=request.user).values('categoria').annotate(total=Sum('valor')).order_by('categoria'):
            lbls.append(Categoria.objects.get(pk=i['categoria']).descricao)
            values.append(i['total'])
        data = {
            "labels": lbls,
            'values': values
        }
        return JsonResponse(data)