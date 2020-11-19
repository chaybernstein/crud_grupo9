from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

from . import models
from . import forms


# classe em comum com Criar e Editar pra usar um model só
class BaseUsuario(View):
    template_name = 'usuario/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'userform': forms.UserForm(
                data=self.request.POST or None),
            'usuarioform': forms.UserForm(
                data=self.request.POST or None)
        }
        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BaseUsuario):
    pass


class Editar(BaseUsuario):
    def get(self, *args, **kwargs):
        return HttpResponse('Editar')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
