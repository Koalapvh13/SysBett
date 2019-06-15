from django.contrib.auth import login, logout
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from appGastos.reports import Render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from appGastos.form import *

# Create your views here.
from appGastos.customAuthUser import CustomAuthUser


def do_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            auth = CustomAuthUser().authenticate(email=request.POST['email'], senha=request.POST['senha'])
            if auth is not None:
                login(request, auth)
                return HttpResponseRedirect('/')
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
        if salva.is_valid():
            despesa = salva.save(commit=False)
            despesa.usuario = request.user
            despesa.tipo = 1
            despesa.save()
            return HttpResponseRedirect('/receita')
    dicio = {"form": TransacaoForm(), "title": "Cadastrar Despesa", 'urli': 'despesa'}
    return render(request, 'appGastos/cadTransacao.html', dicio)


@login_required
def listagem_despesa(request):
    salvo = False
    if request.GET.get("st") == "0":
        salvo = True

    dicio = {"transacao": Transacao.objects.filter(tipo="1", usuario=request.user).order_by('-data'),
             "lenT": len(Transacao.objects.filter(tipo="1", usuario=request.user).order_by('data')),
             'urli': 'despesa',
             "title": "Despesa",
             "salvo": salvo}
    return render(request, 'appGastos/listagem.html', dicio)


@login_required
def listagem_receita(request):
    salvo = False
    if request.GET.get("st") == "0":
        salvo = True

    dicio = {"transacao": Transacao.objects.filter(tipo="0", usuario=request.user).order_by('-data'),
             "lenT": len(Transacao.objects.filter(tipo="0", usuario=request.user).order_by('data')),
             'urli': 'receita',
             "title": "Receita",
             "salvo": salvo}
    return render(request, 'appGastos/listagem.html', dicio)


@login_required
def descricao_conta(request, idit):
    tipo = Transacao.objects.get(pk=idit).tipo
    print(tipo)
    if request.method == 'POST':
        salva = TransacaoForm(request.POST, instance=Transacao.objects.get(pk=idit))
        if salva.is_valid():
            salva.save()
            if tipo == "0":
                return HttpResponseRedirect('/listareceitas/?st=0')
            else:
                return HttpResponseRedirect('/listadespesas/?st=0')
        else:
            pass
    if tipo == "0":
        dicio = {
            "form": TransacaoForm(instance=Transacao.objects.get(pk=idit)),
            "title": "Atualizar Receita",
            'urli': 'decreceita',
            'id_reg': idit}
    else:
        dicio = {
            "form": TransacaoForm(instance=Transacao.objects.get(pk=idit)),
            "title": "Atualizar registro",
            'urli': 'decdespesa',
            'id_reg': idit}
    return render(request, 'appGastos/item.html', dicio)


@login_required
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

        for i in Transacao.objects.filter(tipo=tipo_transacao, usuario=request.user).values('categoria').annotate(
                total=Sum('valor')).order_by('categoria'):
            lbls.append(Categoria.objects.get(pk=i['categoria']).descricao)
            values.append(i['total'])
        data = {
            "labels": lbls,
            'values': values
        }
        return JsonResponse(data)


@login_required
def api_values(request):
    if request.user.is_authenticated:
        try:
            receita = Transacao.objects.filter(tipo=0, usuario=request.user)
            despesa = Transacao.objects.filter(tipo=1, usuario=request.user)

            val_receita = 0
            val_despesa = 0

            for i in receita:
                val_receita += i.valor

            for j in despesa:
                val_despesa += j.valor

            data = {
                "receita": val_receita,
                "despesa": val_despesa,
                "saldo": val_receita-val_despesa
            }
            return JsonResponse(data)
        except Exception:
            data = {
                "erro": Exception,
            }
            return JsonResponse(data)



@login_required
def pagepdf(request):
    sales = Transacao.objects.all()
    today = timezone.now()
    params = {
        'today': today,
        'sales': sales,
        'request': request
    }
    return Render.render('appGastos/pdf.html', params)
