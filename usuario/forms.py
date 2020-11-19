from django import forms
from django.contrib.auth.models import User
from . import models


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = models.Usuario
        fields = '__all__'
        # exclude = ('usuario',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password',
                 'email')  # campos exibidos para o usuário

    def clean(self, *args, **kwargs):
        # data = dados crus do formulário / cleaned = dados limpos do formulário
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}
