from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render

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