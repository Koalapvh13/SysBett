from django.contrib import admin
from django.urls import path, include

from usuario.views import *


urlpatterns = [
    path('users/', cadastro_usuario, name='users'),
    path('edit_user/', edita_usuario, name='conf'),
    path('login/', do_login, name='login'),
    path('logout/', do_logout, name='logout'),
]
