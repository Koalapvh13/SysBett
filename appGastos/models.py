from datetime import datetime

from django.db import models
from usuario.models import Usuarios
# Create your models here.


class Categoria(models.Model):
    descricao = models.CharField(max_length=50, verbose_name="Descrição")
    tipo = models.CharField(max_length=50, verbose_name="Tipo")

    def __str__(self):
        return self.descricao


class Transacao(models.Model):
    descricao = models.CharField(max_length=90, verbose_name="Descrição")
    valor = models.FloatField(verbose_name="Valor")
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    data = models.DateField(verbose_name="Data", default=datetime.today)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, verbose_name="Tipo", choices=[('0', 'Receita'), ('1', 'Despesa')])

    def __str__(self):
        return self.descricao