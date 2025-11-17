from django.db import models
from .amostra import Amostra
from .parametro import Parametro

class ParametroAmostra(models.Model):
    amostra = models.ForeignKey(
        Amostra,
        on_delete=models.CASCADE,
        related_name="parametros_amostra"
    )

    parametro = models.ForeignKey(
        Parametro,
        on_delete=models.CASCADE
    )

    analisar = models.BooleanField(default=True, verbose_name="Será analisado?")
    resultado = models.CharField(max_length=100, null=True, blank=True, verbose_name="Resultado")

    def __str__(self):
        return f"{self.amostra.identificacao} - {self.parametro.descricao}"

    class Meta:
        unique_together = ("amostra", "parametro")
        verbose_name = "Parâmetro da Amostra"
        verbose_name_plural = "Parâmetros da Amostra"