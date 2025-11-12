from django.db import models

from . import Matriz
from .empresa import Empresa
from .servico import Servico


class OrdemServico(models.Model):
    data_emissao = models.DateField(auto_now_add=True, verbose_name="Data de Emissão")
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, verbose_name="Empresa Cliente"
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    servicos = models.ManyToManyField(
        Servico,
        blank=False,
        help_text="Selecione os serviços desta OS",
        verbose_name="Serviços contratados",
    )
    resultados_servicos = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"OS {self.id} - {self.empresa}"


    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
