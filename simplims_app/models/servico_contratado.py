from django.db import models
from .ordem_servico import OrdemServico
from .servico import Servico

class ServicoContratado(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
    )

    quantidade_amostras = models.PositiveIntegerField(default=2)

    def __str__(self):
        return f"({self.ordem_servico.id}) {self.servico.descricao}"