from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from usuario.form import *
from usuario.customAuthUser import CustomAuthUser
from usuario.models import Usuarios


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
        return render(request, 'usuario/signin.html', {'form': LoginForm(), "salvo": salvo})
    return HttpResponseRedirect('/')


@login_required
def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login')



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
            return render(request, 'usuario/signup.html', dicio)
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
            return render(request, 'usuario/confuser.html', dicio)
    return HttpResponseRedirect("/")
