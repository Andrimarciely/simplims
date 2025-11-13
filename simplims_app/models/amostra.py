from django.db import models
from .servico_contratado import ServicoContratado

class Amostra(models.Model):

    servico_contratado = models.ForeignKey(
        'ServicoContratado',
        on_delete=models.CASCADE,
        related_name='amostras',
    )

    identificacao = models.CharField(
        max_length=50,
        verbose_name='Identificação',
        editable=False  # impede que o usuário altere manualmente
    )

    data_coleta = models.DateField(
        verbose_name='Data da Coleta'
    )

    hora_coleta = models.TimeField(
        verbose_name='Hora da Coleta',
        blank=True,
        null=True
    )

    local_coleta = models.CharField(
        max_length=100,
        verbose_name='Local da Coleta'
    )

    class Meta:
        verbose_name = 'Amostra'
        verbose_name_plural = 'Amostras'
        ordering = ['-data_coleta', 'identificacao']

    def __str__(self):
        return f"{self.identificacao}"

    def save(self, *args, **kwargs):
        # Gera automaticamente a identificação se ainda não existir
        if not self.identificacao:
            prefixo = "MJ-"
            # Conta quantas amostras já existem para esse serviço
            total = Amostra.objects.filter(servico_contratado=self.servico_contratado).count() + 1
            self.identificacao = f"{prefixo}-{total:03d}"
        super().save(*args, **kwargs)
