from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

import re
from utils.validacpf import valida_cpf


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,
                                   verbose_name='Usuário')  # quando usuario for deletado CASCADE
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)  # sem caracteres apenas números
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)  # apenas números
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='RS',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.usuario} '

    # validação CPF e CEP
    def clean(self):
        error_messages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        usuario = Usuario.objects.filter(cpf=cpf_enviado).first()

        if usuario:
            cpf_salvo = usuario.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF já cadastrado.'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'CPF inválido, digite somente os 11 números.'

        if re.search(r'[^0-9]', self.cep) or len(
                self.cep) < 8:  # valida se CEP tem apenas números usando uma expressão regular
            error_messages['cep'] = 'CEP inválido, digite somente os 8 números.'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
