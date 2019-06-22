"""sysbett URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appGastos.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('relatorio/', gen_report, name='relatorio'),
    path('despesa/', cadastro_despesa, name='despesa'),
    path('receita/', cadastro_receita, name='receita'),
    path('users/', cadastro_usuario, name='users'),
    path('edit_user/', edita_usuario, name='conf'),
    path('login/', do_login, name='login'),
    path('', index, name="mainpage"),
    path('/', index, name="mainpage"),
    path('add/', categoriasadd),
    path('pdf/', pagepdf),
    path('listadespesas/', listagem_despesa,  name="listadespesa"),
    path('listareceitas/', listagem_receita,  name="listareceita"),
    path('api/transacao/<slug:transacao>/', api_transacoes),
    path('api/valores/', api_values),
    path('receitas/<int:idit>', descricao_conta, name="decreceita"),
    path('despesas/<int:idit>', descricao_conta, name="decdespesa"),
    path('transacao/<int:idit>', deletar_transacao, name="deletar"),
    path('logout/', do_logout, name='logout'),
]
