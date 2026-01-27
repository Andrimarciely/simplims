from django.db import models
from .empresa import Empresa

class ClienteSistema(models.Model):
    """
    Representa o CLIENTE DO SIMPLIMS (tenant).
    Normalmente é uma consultoria ambiental.
    """

    empresa = models.OneToOneField(
        Empresa,
        on_delete=models.CASCADE,
        related_name='cliente_sistema',
        limit_choices_to={'tipo': 'consultoria'}
    )

    slug = models.SlugField(
        unique=True,
        help_text='Identificador usado na URL (ex: acme)'
    )

    ativo = models.BooleanField(default=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente do Sistema'
        verbose_name_plural = 'Clientes do Sistema'

    def __str__(self):
        return f'{self.empresa.nome} ({self.slug})'
