from django.db import models

from simplims_app.models import Matriz


class Servico(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    matriz = models.ForeignKey(
        Matriz,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.descricao} | {self.matriz}"

    class Meta:
        verbose_name = "Serviço"
