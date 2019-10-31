from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.admin import UserAdmin
from django import forms
from appGastos.models import *

admin.site.register(Categoria)
admin.site.register(Transacao)
