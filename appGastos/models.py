from datetime import datetime

from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, nome, email=None, password=None):
        if not nome:
            raise ValueError("O nome Informado Não é Válido!")
        if not password:
            raise ValueError("A Senha Não é Válida!")
        user = self.model(nome=nome, email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_user(self, nome, email=None, password=None):
        return self._create_user(nome, email, password)

    def create_superuser(self, nome, email=None, password=None):
        user = self._create_user(nome, email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuarios(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=80, verbose_name="Nome", default=None)
    email = models.CharField(max_length=45, unique=True, verbose_name="E-mail")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UserManager()


# todo - ADD CLASS CATEGORIA
class Categoria(models.Model):
    descricao = models.CharField(max_length=50, verbose_name="Descrição")
    tipo = models.CharField(max_length=50, verbose_name="Tipo")


# todo - ADD CLASS TRANSAÇÃO
class Transacao(models.Model):
    descricao = models.CharField(max_length=90, verbose_name="Descrição")
    valor = models.FloatField(verbose_name="Valor")
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    data = models.DateField(verbose_name="Data", default=datetime.today)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, verbose_name="Tipo", choices=[(0, 'Receita'), (1, 'Despesa')])


# todo - ADD CLASS RELATÓRIO
class Relatorio(models.Model):
    pass