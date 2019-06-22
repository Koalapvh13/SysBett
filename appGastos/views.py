import re

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
    salvo = False
    if request.GET.get("st") == "1":
        salvo = True
    if not request.user.is_authenticated:
        if request.method == 'POST':
            auth = CustomAuthUser().authenticate(email=request.POST['email'], senha=request.POST['senha'])
            if auth is not None:
                login(request, auth)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login/?st=1')
        return render(request, 'appGastos/signin.html', {'form': LoginForm(), "salvo": salvo})
    return HttpResponseRedirect('/')


@login_required
def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login')


def index(request):
    if request.user.is_authenticated:
        dicio = {"transacao": Transacao.objects.filter(usuario=request.user).order_by('-id'),
                 "lenT": len(Transacao.objects.filter(usuario=request.user).order_by('data')),
                 "title": "Receitas"}
        return render(request, 'appGastos/dashboard.html', dicio)
    else:
        return render(request, 'appGastos/index.html')


def cadastro_usuario(request):
    salvo = False
    if request.GET.get("st") == "0":
        salvo = True
    if not request.user.is_authenticated:
        if request.method == 'POST':
            salva = CustomUserCreationForm(request.POST)
            salva.is_valid()
            salva.save()
            return HttpResponseRedirect("/users/?st=0")
        else:
            dicio = {"form": CustomUserCreationForm(), "title": "Cadastrar Usuário", 'urli': "users", "salvo": salvo}
            return render(request, 'appGastos/signup.html', dicio)
    return HttpResponseRedirect("/")


@login_required
def edita_usuario(request):
    salvo = False
    if request.GET.get("st") == "0":
        salvo = True
    if request.user.is_authenticated:
        if request.method == 'POST':
            salva = CustomUserCreationForm(request.POST, instance=Usuarios.objects.get(pk=request.user.id))
            salva.is_valid()
            salva.save()
            auth = CustomAuthUser().authenticate(email=request.POST['email'], senha=request.POST['password1'])
            if auth is not None:
                login(request, auth)
            return HttpResponseRedirect("/edit_user/?st=0")
        else:
            dicio = {"form": CustomUserCreationForm(instance=Usuarios.objects.get(pk=request.user.id)),
                     "title": "Editar Usuário", 'urli': "conf", "salvo": salvo}
            return render(request, 'appGastos/confuser.html', dicio)
    return HttpResponseRedirect("/")


@login_required
def gen_report(request):
    if request.method == 'POST':
        inicial = request.POST['data_inicial']
        final = request.POST['data_final']
        print(inicial, final)
        print(request.POST['data_inicial'])
        return HttpResponseRedirect("/pdf/?ini="+inicial+"&end="+final)
    dicio = {"form": RelatorioGeral(), "title": "Gerar Relatório Geral", 'urli': 'relatorio'}
    return render(request, 'appGastos/genReport.html', dicio)


@login_required
def cadastro_receita(request):
    salvo = False
    if request.GET.get("st") == "0":
        salvo = True
    if request.user.is_authenticated and request.method == 'POST':
        salva = TransacaoReceitaForm(request.POST)
        if salva.is_valid():
            receita = salva.save(commit=False)
            receita.usuario = request.user
            receita.tipo = 0
            receita.save()
            return HttpResponseRedirect('/receita/?st=0')
    dicio = {"form": TransacaoReceitaForm(), "title": "Cadastrar Receita", 'urli': 'receita', "salvo": salvo}
    return render(request, 'appGastos/cadTransacao.html', dicio)


@login_required
def cadastro_despesa(request):
    salvo = False
    if request.GET.get("st") == "0":
        salvo = True
    if request.user.is_authenticated and request.method == 'POST':
        salva = TransacaoDespesaForm(request.POST)
        if salva.is_valid():
            despesa = salva.save(commit=False)
            despesa.usuario = request.user
            despesa.tipo = 1
            despesa.save()
            return HttpResponseRedirect('/despesa/?st=0')
    dicio = {"form": TransacaoDespesaForm(), "title": "Cadastrar Despesa", 'urli': 'despesa', "salvo": salvo}
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
        if tipo == "0":
            salva = TransacaoReceitaForm(request.POST, instance=Transacao.objects.get(pk=idit))
            if salva.is_valid():
                salva.save()
            return HttpResponseRedirect('/listareceitas/?st=0')
        else:
            salva = TransacaoDespesaForm(request.POST, instance=Transacao.objects.get(pk=idit))
            if salva.is_valid():
                salva.save()
            return HttpResponseRedirect('/listadespesas/?st=0')
    else:
        pass
    if tipo == "0":
        dicio = {
            "form": TransacaoReceitaForm(instance=Transacao.objects.get(pk=idit)),
            "title": "Atualizar Receita",
            'urli': 'decreceita',
            'id_reg': idit}
    else:
        dicio = {
            "form": TransacaoDespesaForm(instance=Transacao.objects.get(pk=idit)),
            "title": "Atualizar registro",
            'urli': 'decdespesa',
            'id_reg': idit}
    return render(request, 'appGastos/item.html', dicio)


@login_required
def deletar_transacao(request, idit):
    salvo = False
    if request.GET.get("st") == "0":
        salvo = True

    tipo = Transacao.objects.get(pk=idit).tipo
    Transacao.objects.get(pk=idit).delete()
    if tipo == "0":
        return HttpResponseRedirect('/listareceitas')
    else:
        return HttpResponseRedirect('/listadespesas')


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
                "saldo": round(val_receita - val_despesa, 2)
            }
            return JsonResponse(data)
        except Exception:
            data = {
                "erro": Exception,
            }
            return JsonResponse(data)


@login_required
def pagepdf(request):
    min_date = request.GET.get("ini")
    max_date = request.GET.get("end")

    lista_receita = Transacao.objects.filter(tipo="0", usuario=request.user, data__gte=min_date, data__lte=max_date).order_by('-data')
    lista_despesa = Transacao.objects.filter(tipo="1", usuario=request.user, data__gte=min_date, data__lte=max_date).order_by('-data')

    receita = Transacao.objects.filter(tipo=0, usuario=request.user, data__gte=min_date, data__lte=max_date)
    despesa = Transacao.objects.filter(tipo=1, usuario=request.user, data__gte=min_date, data__lte=max_date)

    val_receita = 0
    val_despesa = 0

    for i in receita:
        val_receita += i.valor

    for j in despesa:
        val_despesa += j.valor

    params = {
        'ini': min_date[8:10]+"/"+min_date[5:7]+"/"+min_date[0:4],
        'end': max_date[8:10]+"/"+max_date[5:7]+"/"+max_date[0:4],
        'lreceita': lista_receita,
        'ldespesa': lista_despesa,
        'request': request,
        'receita': val_receita,
        'despesa': val_despesa,
        'saldo': round(val_receita - val_despesa, 2)
    }
    return Render.render('appGastos/pdf.html', params)


def categoriasadd(request):
    receita = ['Salário', 'Outras Receitas']
    despesa = ['Alimentação', 'Sobrevivência', 'Aluguel', 'Combustível', 'Educação', 'Lazer', 'Supermercado', 'Vestuário', 'Saúde', 'Comunicação', 'Água e Esgoto', 'Luz', 'Outros']

    try:
        for i in receita:
            Categoria.objects.create(descricao=i, tipo="Receita")

        for j in despesa:
            Categoria.objects.create(descricao=j, tipo="Despesa")
        return HttpResponseRedirect("/")
    except Exception:
        return HttpResponseRedirect("/login")