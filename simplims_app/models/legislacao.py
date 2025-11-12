from django.db import models

from simplims_app.models import Parametro


class Legislacao(models.Model):
    parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE)
    valor_maximo = models.FloatField(null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.parametro.descricao}"
