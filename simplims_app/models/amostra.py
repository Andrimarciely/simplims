from django.db import models
from .servico_contratado import ServicoContratado
from .categoria_parametro import CategoriaParametro

class Amostra(models.Model):
    servico_contratado = models.ForeignKey(
        ServicoContratado,
        on_delete=models.CASCADE,
        null=False,  # se não permitir nulo, é obrigatório
        blank=False
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

    TIPO_PONTO = (
        ("MONTANTE", "Montante"),
        ("JUSANTE", "Jusante"),
        ("NA", "Não se aplica"),
    )

    tipo_ponto = models.CharField(
        max_length=10,
        choices=TIPO_PONTO,
        verbose_name="Ponto (Montante/Jusante/Não se aplica)"
    )

    categorias = models.ManyToManyField(
        CategoriaParametro,
        blank=True,
        related_name="amostras",
        verbose_name="Categorias de Parâmetros"
    )

    class Meta:
        verbose_name = 'Amostra'
        verbose_name_plural = 'Amostras'
        ordering = ['-data_coleta', 'identificacao']

    def __str__(self):
        return f"{self.identificacao}"

    def save(self, *args, **kwargs):
        if not self.identificacao:
            # Conta quantas amostras existem no banco
            total = Amostra.objects.count() + 1
            self.identificacao = f"MJ-{total:03d}"
        super().save(*args, **kwargs)
