# models/servico_contratado.py
from django.db import models
from .ordem_servico import OrdemServico
from .servico import Servico


class ServicoContratado(models.Model):
    """
    Modelo intermediário que registra cada serviço contratado em uma ordem de serviço.
    Permite rastrear o status individual de cada serviço.
    """

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='servicos_contratados',
        verbose_name="Ordem de Serviço"
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name='contratacoes',
        verbose_name="Serviço"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )

    data_inicio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Início"
    )

    data_conclusao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão"
    )

    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações do Serviço"
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Serviço Contratado"
        verbose_name_plural = "Serviços Contratados"
        unique_together = ['ordem_servico', 'servico']  # Evita duplicação
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.servico.nome} - OS #{self.ordem_servico.id} - {self.get_status_display()}"
