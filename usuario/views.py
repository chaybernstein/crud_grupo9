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

        self.usuario = None


        # se usuário está logado
        if self.request.user.is_authenticated:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.usuario,
                    instance=self.request.usuario,
                ),
                'usuarioform': forms.UserForm(
                    data=self.request.POST or None,
                    instance=self.request.user,
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None),
                'usuarioform': forms.UserForm(
                    data=self.request.POST or None)
            }
        self.userform = self.contexto['userform']
        self.usuarioform = self.contexto['usuarioform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BaseUsuario):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.usuarioform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )

            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username)

            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.usuario:
                self.usuarioform.cleaned_data['usuario'] = usuario
                print(self.usuarioform.cleaned_data)
                perfil = models.Usuario(**self.usuarioform.cleaned_data)
                perfil.save()
            else:
                perfil = self.usuarioform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        # Usário não logado (novo)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.usuarioform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )

            if autentica:
                login(self.request, user=usuario)

        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        return self.renderizar

class Editar(BaseUsuario):
    def get(self, *args, **kwargs):
        return HttpResponse('Editar')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:criar')

        usuario = authenticate(
            self.request, username=username, password=password)

        if not usuario:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:criar')

        login(self.request, user=usuario)


class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        logout(self.request)

        self.request.session['carrinho'] = carrinho
        self.request.session.save()
